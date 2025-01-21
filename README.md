# Orders Project

## Описание
Это RESTful-приложение для управления заказами и продуктами. Реализованы следующие возможности:
- CRUD-операции для заказов и продуктов.
- Фильтрация заказов по статусу и диапазону цен.
- Логирование запросов и изменений в заказах.
- Сигналы для событий создания, обновления и удаления заказов.
- Метрики для подсчёта вызовов эндпоинтов, успешных и неуспешных запросов.
- Документация API через Swagger.
- Поддержка Docker для контейнеризации проекта.

---

## Требования
- Python 3.10
- Docker и Docker Compose
- PostgreSQL 14+
- Redis 6+

---

## Установка

### Шаг 1: Установка локально
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Taichilli/TZ_DIGITAL_TRAVEL.git
   cd orders_project
   
Установите виртуальное окружение и активируйте его:
python -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate

Установите зависимости:
pip install -r requirements.txt

Выполните миграции базы данных:
python manage.py migrate

Создайте суперпользователя:
python manage.py createsuperuser

Запустите приложение:
python manage.py runserver

### Шаг 2: 
Установка через Docker
Соберите Docker-образ:
docker build -t orders_project .
Запустите контейнер:
docker run -d -p 8000:8000 orders_project
Приложение будет доступно по адресу: http://127.0.0.1:8000
Использование API
Документация API доступна по адресу: http://127.0.0.1:8000/swagger/

Основные эндпоинты:
/api/products/ — работа с продуктами.
/api/orders/ — работа с заказами (с фильтрацией по статусу, диапазону цен).
/metrics/ — метрики вызовов эндпоинтов.

Метрики
Подсчёт количества вызовов каждого эндпоинта.
Сбор успешных и неуспешных запросов.
Доступ через API /metrics/ или сохранение в логах metrics.log.

События
При изменении состояния заказа выбрасываются события:
Создание заказа (OrderCreated): передаются order_id, status, customer_name, total_price.
Обновление заказа (OrderUpdated): передаются order_id, old_status, new_status.
Удаление заказа (OrderDeleted): передаются order_id, customer_name.
Все события логируются в orders.log.

Тестирование
Запустите тесты:
python manage.py test
Покрытие тестами:
Логирование запросов и действий.
Метрики.
Сигналы на события.

Структура проекта
orders_project/
├── orders/                   # Основное приложение
│   ├── migrations/           # Миграции базы данных
│   ├── models.py             # Модели данных
│   ├── views.py              # Логика API
│   ├── serializers.py        # Сериализация данных
│   ├── signals.py            # Сигналы для событий
│   ├── urls.py               # URL маршруты
│   ├── tests.py              # Тесты
├── orders_project/
│   ├── settings.py           # Настройки проекта
│   ├── urls.py               # Основные маршруты
├── Dockerfile                # Docker-инструкция
├── requirements.txt          # Зависимости
├── README.md                 # Описание проекта
Автор
Разработчик: Чурин Александр Викторович