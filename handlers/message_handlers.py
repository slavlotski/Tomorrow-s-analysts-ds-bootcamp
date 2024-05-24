from telegram import Update
from telegram.ext import ContextTypes
from config.openai_client import client

import requests
from bs4 import BeautifulSoup
import re

async def chatgpt_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Текст входящего сообщения
    text = update.message.text

    # Инициализация или обновление истории сообщений пользователя
    if 'history' not in context.user_data:
        context.user_data['history'] = []

    # Проверка, содержит ли сообщение ссылку
    url_pattern = re.compile(r'https?://\S+')
    url_match = url_pattern.search(text)

    if url_match:
        url = url_match.group(0)

        # Выполнение запроса к странице
        try:
            response = requests.get(url, verify=False)  # Отключение проверки SSL
        except requests.exceptions.SSLError as e:
            await update.message.reply_text(f"Ошибка SSL: {e}", parse_mode="Markdown")
            return

        if response.status_code == 200:
            # Разбор HTML-контента
            soup = BeautifulSoup(response.content, 'html.parser')

            # Извлечение заголовка и контента статьи
            title = soup.find('h1') or soup.find('title')
            content = soup.find('article') or soup.find('div', class_='entry-content') or soup.find('body')

            title_text = title.get_text(strip=True) if title else 'No title'
            content_text = content.get_text(strip=True) if content else 'No content'

            # Определение языка статьи
            language = 'en'
            if re.search(r'[А-Яа-я]', content_text):
                language = 'ru'

            # Формирование контекста для запроса к ChatGPT
            messages = [
                {
                    "role": "system",
                    "content": "Ты референт. Ответь на следующий вопрос в формате Markdown для телеграмм"
                },
                {"role": "user", "content": f"Сделай саммори в формате Markdown для телеграм по следующей статье: \
                Заголовок: {title_text} \
                Текст: {content_text[:2000]} \
                c заголовками к каждому блоку текста. Для заголовков используй \
                следующие формат: *italic*. Саммори должно быть не более 5 предложений. Длина сообщения должна быть не более 4000 символов. Язык саммори должен соответствовать языку статьи."}
            ]

            # Запрос к ChatGPT
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1024,
                temperature=0.0,
            )

            # Ответ
            reply = response.choices[0].message.content.strip()

            # Добавление ответа ассистента в историю
            context.user_data['history'].append({"role": "assistant", "content": reply})

            # Отправка ответа с саммари статьи
            await update.message.reply_text(reply, parse_mode="Markdown")

            print("user:", text)
            print("assistant:", reply)
            return

        else:
            await update.message.reply_text(f"Не удалось загрузить статью. Статус код: {response.status_code}", parse_mode="Markdown")
            return

    # Проверка, запрашивает ли пользователь новости
    if 'загрузи новости' in text.lower():
        # URL страницы
        url = "http://datascientist.one/news/"

        # Выполнение запроса к странице
        try:
            response = requests.get(url, verify=False)  # Отключение проверки SSL
        except requests.exceptions.SSLError as e:
            await update.message.reply_text(f"Ошибка SSL: {e}", parse_mode="Markdown")
            return

        # Проверка успешности запроса
        if response.status_code == 200:
            # Разбор HTML-контента
            soup = BeautifulSoup(response.content, 'html.parser')

            # Поиск всех статей на странице
            articles = soup.find_all('article')

            # Сбор данных из статей, избегая дубликатов
            news_data = []
            seen_links = set()
            for article in articles:
                title_element = article.find('h2', class_='entry-title')
                summary_element = article.find('div', class_='entry-content')
                link_element = article.find('a', class_='read-more-link')

                title = title_element.get_text(strip=True) if title_element else 'No title'
                summary = summary_element.get_text(strip=True) if summary_element else 'No summary'
                link = link_element['href'] if link_element else 'No link'

                if link in seen_links:
                    continue  # Пропустить дубликат
                seen_links.add(link)

                full_text = 'No full text'
                if link != 'No link':
                    article_response = requests.get(link, verify=False)  # Отключение проверки SSL
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.content, 'html.parser')
                        full_text_element = article_soup.find('div', class_='entry-content')
                        full_text = full_text_element.get_text(strip=True) if full_text_element else 'No full text'

                news_data.append({
                    'title': title,
                    'summary': summary,
                    'link': link,
                    'full_text': full_text
                })

            # Сохранение данных в контекст пользователя
            context.user_data['news_data'] = news_data
            context.user_data['history'].append({"role": "system", "content": "Новости успешно загружены."})

            # Ограничиваем количество новостей до 5
            limited_news_data = news_data[:5]
            print(f"Number of news articles: {len(limited_news_data)}")  # Проверка количества новостей

            # Формирование контекста для запроса к ChatGPT
            messages = [
                {
                    "role": "system",
                    "content": "Ты референт. Ответь на следующий вопрос в формате Markdown для телеграмм"
                },
                {"role": "user", "content": f"Сделай саммори в формате Markdown для телеграм по каждой теме из \
                новостей: {limited_news_data} с заголовками к каждому блоку текста. Для заголовков используй \
                следующие формат: *italic*. Каждое саммори должно быть не более 5 предложений. В конце саммори \
                нужно привести ссылку на статью. Длина сообщения должна быть не более 4000 символов."}
            ]

            # Запрос к ChatGPT
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1024,
                temperature=0.0,
            )

            # Ответ
            reply = response.choices[0].message.content.strip()

            # Добавление ответа ассистента в историю
            context.user_data['history'].append({"role": "assistant", "content": reply})

            # Отправка ответа с саммари новостей
            await update.message.reply_text(reply, parse_mode="Markdown")

            print("user:", text)
            print("assistant:", reply)
            return

        else:
            await update.message.reply_text(f"Не удалось загрузить новости. Статус код: {response.status_code}", parse_mode="Markdown")
            return

    # Добавление нового сообщения пользователя в историю
    context.user_data['history'].append({"role": "user", "content": text})

    # Формирование полного контекста для запроса, включая историю сообщений
    messages = [
        {
            "role": "system",
            "content": "Ответь на следующий вопрос в формате Markdown для телеграмм. Ответ давай на языке \
            запроса или на том на котором попросили. Весь ответ должен быть на одном языке. Если начал писать на\
             русском, то продолжай на нем же и т.п. . Длина сообщения должна быть не более 4000 символов."
        }
    ] + context.user_data['history']

    # Если новости загружены и запрос касается новостей, добавляем их к контексту
    if 'news_data' in context.user_data:
        messages.append({"role": "system", "content": "В истории есть загруженные новости. \
                        Учитывай это при ответе."})

    # Запрос к ChatGPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages + [{"role": "user", "content": f"Ответь на следующий вопрос в формате Markdown для \
                                 телеграм {text}. Говорить о том, что ты даешь ответ в формате Markdown не нужно. \
                                 Для заголовков используй следующий формат: *italic*. Если в ответе есть код, \
                                 определяй язык и выделяй его так ```code```. Если в {text} не говорится про \
                                 код, его генерировать не нужно. Сам {text} не повторяй и не перефразируй. \
                                 Никаких дополнительных префиксов типа 'Ответ:' писать не нужно. \
                                 Сразу давай ответ. Длина сообщения должна быть не более 4000 символов."}],
        max_tokens=1024,
        temperature=0.0,
    )

    # Ответ
    reply = response.choices[0].message.content.strip()

    # Добавление ответа ассистента в историю
    context.user_data['history'].append({"role": "assistant", "content": reply})

    # Перенаправление ответа в Telegram
    await update.message.reply_text(reply, parse_mode="Markdown")

    print("user:", text)
    print("assistant:", reply)