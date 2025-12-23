# Дерево подразделений и сотрудников

Веб-страница на Django: древовидная структура подразделений (до 5 уровней) и список сотрудников. Управление записями через админку Django, фронт на Bootstrap.

## Запуск локально
1. Создайте и активируйте виртуальное окружение: `py -3 -m venv .venv && .venv\Scripts\activate`.
2. Установите зависимости: `pip install -r requirements.txt`.
3. Примените миграции: `python manage.py migrate`.
4. Создайте суперпользователя: `python manage.py createsuperuser`.
5. (Опционально) Сгенерируйте данные: `python manage.py seed_demo --departments 25 --employees 50000` (можно уменьшить).
6. Запустите сервер: `python manage.py runserver` и откройте `http://127.0.0.1:8000/`.

## Запуск в Docker
1. Скопируйте `.env.example` в `.env` и при необходимости поправьте значения. Для локальной машины оставьте `POSTGRES_HOST=localhost`; в контейнере web docker-compose подставит `db`.
2. Запустите: `docker-compose up --build`.
3. Веб: `http://127.0.0.1:8000/`, Postgres: `localhost:5432`.
4. Данные Postgres сохраняются в volume `pg_data`, код пробрасывается внутрь `/app`.

## .env настройки
- `DJANGO_SECRET_KEY` — задайте свой уникальный ключ.
- `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` — отладка и список хостов.
- Параметры БД: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`.
- Файл `.env` уже в `.gitignore` и не попадает в репозиторий.

## Что реализовано
- Модели `Department` (MPTT) и `Employee` с индексами на FK, имя, дату приема.
- Админка: древовидный `MPTTModelAdmin` для подразделений, фильтры/поиск для сотрудников.
- Страница `/`: дерево подразделений по умолчанию раскрыто, можно сворачивать; при выборе узла — сотрудники этого узла и потомков с пагинацией.
- Команда `seed_demo` генерирует 25 подразделений (глубина 5) и ≥50k сотрудников (Faker), параметры настраиваются.

## Замечания
- По умолчанию SQLite для быстрого старта; для больших объемов лучше Postgres — поменяйте `DATABASES` в `org_tree/settings.py` или используйте docker-compose.
- Все зависимости указаны в `requirements.txt`.