# SPA веб-приложения

## Предназначение приложения:
- Формированию полезных привычек 
- Для приобретения полезных привычек (Оповещение о них по средствам уведомления от Telegram bot)
- Избавлению от плохих привычек.

### 1. Для запуска приложения необходимо настроить виртуальное окружение и установить все необходимые зависимости с помощью команд:
    Команда для Windows:
        1- python -m venv venv
        2- venv\Scripts\activate
        3- pip install -r requirement.txt

    Команда для Unix:
        1- python3 -m venv venv
        2- source venv/bin/activate 
        3- pip install -r requirement.txt

### 2. Для запуска celery:
        1- celery -A config worker --loglevel=info --pool=eventlet
        2- celery -A config beat -l info -s django

### 3. Для запуска redis:
    Redis официально не поддерживается в Windows: 
        1- Установите WSL2, Ubuntu. Подробности смотрите тут https://redis.io/docs/getting-started/installation/install-redis-on-windows/
        2- sudo apt-get update
        3- sudo service redis-server start
        4- redis-cli
        5- ping
        
        Ответом от сервиса должно быть PONG. Это означает что Redis подключен

    Команда для Unix:
        1- redis-cli

### 4. Для работы с переменными окружениями необходимо заполнить файл
    - .env

### 5. Для запуска приложения: 
    Команда для Windows:
    - python manage.py runserver

    Команда для Unix:
    - python3 manage.py runserver