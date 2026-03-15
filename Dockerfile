FROM python:3.11-slim

# Установка рабочей директории внутри контейнера
# Вся логика backend лежит в папке /app/backend
WORKDIR /app/backend

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование файла зависимостей backend
COPY backend/requirements.txt ./requirements.txt

# Установка Python зависимостей backend
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода backend
COPY backend .

# Открытие порта
EXPOSE 8000

# Команда запуска backend-приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

