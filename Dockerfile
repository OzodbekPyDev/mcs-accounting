FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Очистка кэша apt после установки
RUN apt-get clean

# Настройка переменных окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка рабочего каталога
WORKDIR /code

# Установка зависимостей Python
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . /code/

# Copy entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Создание и использование не-root пользователя
RUN useradd -m user
RUN chown -R user:user /code
USER user

ENTRYPOINT ["./entrypoint.sh"]
