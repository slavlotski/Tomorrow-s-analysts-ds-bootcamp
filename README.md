# Tomorrow-s-analysts-ds-bootcamp
![alt text](ds-bro-avatar.jpg)

[Ссылка на телеграмм-бота](https://t.me/ds_bro_bot)
# Задача:
Повысить эффективность работы Data Scientist'а, используя AI Virtual Assistant. Для решения данной задачи был разработан python приложение, где используется telegram бот "DS-Bro" для входной точки в приложение пользователей и продукты OpenAI в качестве основного движка проекта под капотом.

# Что умеет виртуальный ассистент?
1. Создать дайджест из актуальных новостей и научных статей DS и делать выжимку по каждой статье. Написан парсер, который может работать с любым интернет ресурсом
2. Умеет выполнять генерацию кода по заданию, а также выполнить рефакторинг кода
3. Составить документацию по ссылке репозитория и дать рекомендацию что нужно сделать перед тем как запустить проект
4. Для передышки ассистент умеет присылать мемы про DS, сгенерированный DALL-E AI, и релаксирующие видео


# Структура проекта
```
Tomorrow-s-analysts-ds-bootcamp/
│
├──.github/workflows
│   └─── publish.yml
│
├──ansible
│  ├─── inventory.ini
│  ├─── install-packages.yml
│  ├─── docker-build-pull.yml
│  └─── deploy-virtual-assistant.yml
│
├── config/
│   ├─── openai_client.py
│   ├─── telegram_bot.py
│   └─── tokens.py
│
├── handlers/
│   ├── __init__.py
│   ├── command_handlers.py
│   └── message_handlers.py
│
├── tests/
│   ├── __init__.py
│   └── test_telegram_openai_api.py
│
├── utils/
│   ├── __init__.py
│   └── helpers.py
│
├── app.py
├── Dockerfile
├── pyproject.toml
└── poetry.lock
```
* .github/workflows - github actions для автоматизации CI/CD
* ansible - для автоматизации развертывания приложения на сервере
* config/ - конфигурационные файлы
* handlers/ - обработчики сообщений, файлов, аудио и команд
* utils/ - вспомогательные функции
* app.py - главный файл приложения
* Dockerfile - скрипт для создания Docker образа
* pyproject.toml - зависимости python пакетов
* poetry.lock - для обеспечения согласованности между установленными зависимостями

# Аппаратное обеспечение и установленные приложения на нем:
**Конфигурация аппаратного обеспечения:**
* Операционнация система: Debian GNU/Linux 12 (bookworm)
* Ядро: Linux 6.1.0-9-amd64
* Архитектура: x86-64
* CPU: 2 ядра
* RAM: 4 гигабайта

**Предустановленный софт на сервере:**
* vim
* build-essential
* python3.11
* python3-venv
* docker-ce
* docker-ce-cli
* docker-buildx-plugin
* docker-compose-plugin

**Пакеты python:**
```
annotated-types==0.7.0
anyio==4.3.0
argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
arrow==1.3.0
asttokens==2.4.1
async-lru==2.0.4
attrs==23.2.0
Babel==2.15.0
beautifulsoup4==4.12.3
bleach==6.1.0
certifi==2024.2.2
cffi==1.16.0
chardet==5.2.0
charset-normalizer==3.3.2
comm==0.2.2
debugpy==1.8.1
decorator==5.1.1
defusedxml==0.7.1
distro==1.9.0
executing==2.0.1
fastjsonschema==2.19.1
fqdn==1.5.1
gitdb==4.0.11
GitPython==3.1.43
h11==0.14.0
httpcore==1.0.5
httpx==0.27.0
idna==3.7
ipykernel==6.29.4
ipython==8.24.0
ipywidgets==8.1.2
isoduration==20.11.0
jedi==0.19.1
Jinja2==3.1.4
json5==0.9.25
jsonpointer==2.4
jsonschema==4.22.0
jsonschema-specifications==2023.12.1
jupyter==1.0.0
jupyter-console==6.6.3
jupyter-events==0.10.0
jupyter-lsp==2.2.5
jupyter_client==8.6.2
jupyter_core==5.7.2
jupyter_server==2.14.0
jupyter_server_terminals==0.5.3
jupyterlab==4.2.1
jupyterlab_pygments==0.3.0
jupyterlab_server==2.27.2
jupyterlab_widgets==3.0.10
MarkupSafe==2.1.5
matplotlib-inline==0.1.7
mistune==3.0.2
nbclient==0.10.0
nbconvert==7.16.4
nbformat==5.10.4
nest-asyncio==1.6.0
notebook==7.2.0
notebook_shim==0.2.4
openai==1.30.2
overrides==7.7.0
packaging==24.0
pandocfilters==1.5.1
parso==0.8.4
pexpect==4.9.0
platformdirs==4.2.2
prometheus_client==0.20.0
prompt-toolkit==3.0.43
psutil==5.9.8
ptyprocess==0.7.0
pure-eval==0.2.2
pycparser==2.22
pydantic==2.7.1
pydantic_core==2.18.2
Pygments==2.18.0
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
python-json-logger==2.0.7
python-telegram-bot==21.2
PyYAML==6.0.1
pyzmq==26.0.3
qtconsole==5.5.2
QtPy==2.4.1
referencing==0.35.1
requests==2.32.2
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rpds-py==0.18.1
Send2Trash==1.8.3
six==1.16.0
smmap==5.0.1
sniffio==1.3.1
soupsieve==2.5
stack-data==0.6.3
terminado==0.18.1
tinycss2==1.3.0
tornado==6.4
tqdm==4.66.4
traitlets==5.14.3
types-python-dateutil==2.9.0.20240316
typing_extensions==4.12.0
uri-template==1.3.0
urllib3==2.2.1
wcwidth==0.2.13
webcolors==1.13
webencodings==0.5.1
websocket-client==1.8.0
widgetsnbextension==4.0.10
```
# Деплой приложения через CI/CD
Сборка и развертывание приложения осуществляется с помощью github actions. Каждый этап описан инструкциями в файле *.github/workflows/publish.yml*. Для обеспечения более тонкой настройки и возможности развертывания приложения на сервер используются ansible playbook'и. Само приложение, все его зависимости и код собираются в docker image и публикуется в публичный docker hub. Для запуска приложения используется docker container.

## Этапы CI/CD:
1. Сборка и установка приложений на удаленный сервер с помощью ansible playbook *"install-packages.yml"*
2. Подготовка директории проекта, создание .env файла с секретами, проверка на наличие значений в docker_user, doker_token для входа в docker hub, сборка всех необходимых зависимостей приложения через Dockerfile, создание docker image, публикация образа в docker hub осуществляется ansible playbook *"docker-build-pull.yml"*
3. Запуск автотестов pytests с помощью github actions для проверки доступности telegram API и OpenAI API
4. Остановка работающего контейнера на удаленном сервере, удаление неактуального docker образа приложения, скачивание docker образа с docker hub и запуск приложения, используя новый docker image осуществляется ansible playbook *"deploy-virtual-assistant.yml"*
