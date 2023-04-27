# Foodgram
Проект, разработанный в рамках выпускной(дипломной) работы в яндекс.практикум по программе бекенд-python разработчик.
Под готовый фронт на react - с нуля было написано API, опираясь на ТЗ и документацию redoc. Проект запускается в трех контейнерах:
- backend
- nginx
- db (PostgresQL database)
\
контейнер frontend после запуска подготавливает файлы и останавливается.

Ниже приведены основные используемые технологии и библиотеки.


## Технологии
- [Django] - Бэкэнд фреймворк
- [Django Rest Framework] - Фрэймворк для создания API на основе Django
- [Djoser] - Библиотека для авторизации
- [Django Filter] - Библиотека для фильтрации данных
- [Pillow] - Библиотека для обработки изображений
- [Docker] - ПО для развертывания в контейнере
- [Reactjs] - JavaScript-библиотека с открытым исходным кодом для разработки пользовательских интерфейсов.
- [Gunicorn] - WSGI веб-сервер
- [Postgresql] - База данных
- [Nginx] - HTTP Веб-сервер

## Установка

### Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:pmmakovk/foodgram-project-react.git
```
```
cd foodgram-project-react
```
### Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate (Windows)
source venv/bin/activate (Linux)
```
### Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r backend/requirements.txt
```
### Наполнить .env файл
```
cd infra

DB_ENGINE=<...> # указываем, что работаем с postgresql
DB_NAME=<...> # имя базы данных
POSTGRES_USER=<...> # логин для подключения к базе данных
POSTGRES_PASSWORD=<...> # пароль для подключения к БД (установите свой)
DB_HOST=<...> # название сервиса (контейнера)
DB_PORT=<...> # порт для подключения к БД
```
### Перейти в папку с docker-compose.yml и собрать контейнеры:
```
cd infra
docker-compose up --build
```
### Создать миграции, провести их, собрать статику, создать суперюпользователя
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
```

## Примеры запросов к API и ответов
### Доступно на http://localhost/api/docs/redoc.html

