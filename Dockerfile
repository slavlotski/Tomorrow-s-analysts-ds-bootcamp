FROM python:3.9
WORKDIR /app

# копируем файл зависимостей и устанавливаем их
COPY  ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false \
&& poetry install --without dev

# Копируем остальные файлы проекта в контейнер
COPY config/ ./config/
COPY handlers/ ./handlers/
COPY utils/ ./utils/
COPY app.py .

# команда запуска приложения
CMD ["python", "app.py"]