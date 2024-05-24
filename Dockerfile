ARG TELEGRAM_BOT_TOKEN
ARG OPENAI_API_KEY

FROM python:3.9
WORKDIR /app

# копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY config/ ./config/
COPY handlers/ ./handlers/
COPY utils/ ./utils/
COPY app.py .

ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN} \
    OPENAI_API_KEY=${OPENAI_API_KEY}

# команда запуска приложения
CMD ["python", "app.py"]