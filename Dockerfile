# Используем официальный образ Python
FROM python:3.10-slim

# Указываем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \libpq-dev \build-essential

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Установка БД PostgresQL
RUN apt-get update && apt-get install -y postgresql-client

# Копируем все файлы проекта в контейнер
COPY . /app/

# порт, который будет использовать контейнер
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
