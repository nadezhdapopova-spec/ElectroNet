![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2.8-green)

## ElectroNet

**REST API и админ-панель для управления иерархической сетью по продаже электроники.**

Проект реализован в рамках тестового задания и демонстрирует:
- работу с иерархическими структурами
- кастомные permission-классы
- ограничение бизнес-логики на уровне API
- CI/CD пайплайн

### Технологический стек

- Python 3.12

- Django 5.2.8

- Django REST Framework 3.16.1

- PostgreSQL

- DRF-spectacular (Swagger / Redoc)

- Pytest-django

- Coverage

- Flake8, black, isort

### Архитектура проекта

Проект построен по стандартной архитектуре Django:

    config/                 # Конфигурация проекта
    network_node/           # Основное приложение
        models.py
        serializers.py
        permissions.py
        views.py
        urls.py
        admin.py
        tests.py
        management/
            commands/
                seed_data.py


#### Основные сущности

**_NetworkNode_** — звено сети

**_Product_** — продукт

**_Address_** — адрес звена сети

#### Иерархическая структура сети

Сеть имеет 3 уровня:

| Уровень | Тип                            |
| ------- | ------------------------------ |
| 0       | Завод                          |
| 1       | Розничная сеть                 |
| 2       | Индивидуальный предприниматель |

Уровень определяется не названием, а положением в иерархии:

- Завод не имеет поставщика → уровень 0

- Если объект ссылается на завод → уровень 1

- Если объект ссылается на звено уровня 1 → уровень 2

Каждое звено может ссылаться только на одного поставщика.

#### Модель данных

**_NetworkNode_**

name

email

supplier (ForeignKey на self)

debt (Decimal, 2 знака после запятой)

level (вычисляется автоматически)

created_at (auto_now_add)

address (ForeignKey)

**_Address_**

country

city

street

house_number

**_Product_**

name

model

release_date

node (ForeignKey на NetworkNode)

#### ER-диаграмма

    NetworkNode
     ├── supplier → NetworkNode (self FK)
     ├── address → Address
     └── products → Product

#### Права доступа

Реализован кастомный permission-класс DRF.

Доступ к API имеют только:

- авторизованные (is_authenticated=True)

- активные (is_active=True)

- сотрудники (is_staff=True)

#### API

Реализован CRUD для модели NetworkNode.

Ограничение для поля debt (заложенность):

- Нельзя обновлять через API (PUT / PATCH)

- Нельзя изменять при создании (read-only)

- Можно просматривать

- Управляется только через админ-панель или внутреннюю бизнес-логику

Реализовано через:

```
read_only_fields = ("debt",)
```

#### Фильтрация

- Фильтрация по стране (API)

- Фильтрация по городу (админ-панель)

- Фильтрация по уровню в иерархической структуре сети

#### Админ-панель

Реализовано:

- Отображение всех звеньев сети

- Кликабельная ссылка на поставщика

- Фильтр по городу

- Admin action для очистки задолженности

- Просмотр связанных продуктов

#### Эндпоинты

| Метод  | URL                 | Описание             |
| ------ | ------------------- | -------------------- |
| POST   | /api/token/         | Получение JWT        |
| POST   | /api/token/refresh/ | Обновление JWT       |
| GET    | /api/nodes/         | Список узлов         |
| POST   | /api/nodes/         | Создание узла        |
| GET    | /api/nodes/{id}/    | Детальный просмотр   |
| PUT    | /api/nodes/{id}/    | Полное обновление    |
| PATCH  | /api/nodes/{id}/    | Частичное обновление |
| DELETE | /api/nodes/{id}/    | Удаление             |
| GET    | /swagger/           | Swagger              |
| GET    | /redoc/             | ReDoc                |
| GET    | /admin/             | Админка              |

**Пример создания объекта сети**
```
POST /api/nodes/

{
  "name": "Retail Network 1",
  "email": "retail@example.com",
  "supplier": 1,
  "address": 2
}

Ответ:

{
  "id": 5,
  "name": "Retail Network 1",
  "level": 1,
  "debt": "0.00",
  ...
}
```

### Документация API

Swagger UI:
```
/swagger/
```

Redoc UI:
```
/redoc/
```

### Тестирование

Unit тесты реализованы с помощью pytest-django

Запуск тестов
```bash
pytest
```

Отчет покрытия
``` bash
poetry run coverage
```

## Установка и локальный запуск

1. Клонируйте репозиторий
```
git clone https://github.com/nadezhdapopova-spec/ElectroNet.git
cd electronet
```
2. Установите зависимости

Через Poetry:
```
poetry install
```

Через pip:
```
pip install -r requirements.txt
```

3. Заполните .env
````
env.sample

SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=your_database_name_here
DB_USER=your_database_user_here
DB_PASSWORD=your_database_password_here
DB_HOST=localhost
DB_PORT=5432

DJANGO_LOG_LEVEL=INFO
````
4. Создайте базу PostgreSQL

5. Выполните миграции
```
python manage.py migrate
```

6. Создайте суперпользователя
```
python manage.py createsuperuser
```

7. Запустите сервер
```
python manage.py runserver
```

8. Выполните Seed-команду для генерации тестовых данных

Создаются:

- тестовый пользователь (активный, сотрудник)

- адреса

- завод

- розничная сеть

- продукт

```
python manage.py seed_data
```

## Запуск проекта на удаленном сервере

Проект развёртывается на удалённом сервере с помощью Docker Compose и GitHub Actions.

**Адрес сервера с развернутым приложением:** https://diploma.creepysnakes.su/

### Архитектура

Client → Nginx → Gunicorn → Django → PostgreSQL

### Настройка удалённого сервера

**На сервере должны быть установлены:**
````
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx
````

**Дополнительно:**

- пользователь добавлен в группу docker

- вход по SSH-ключу

- открыты порты 80, 443, 22

### Переменные окружения

**Файл .env:**

- не коммитится в репозиторий

- используется на сервере и создаётся автоматически в GitHub Actions

Изменения в файле .env:
````
DEBUG=False
DB_HOST=db
DOCKER_HUB_USERNAME=your_docker_hub_username_here
DOCKER_HUB_TAG=docker_hub_electronet_image_tag_here
BASE_SERVER_URL=localhost
````

### GitHub Secrets

В репозитории → Settings → Secrets and variables → Actions должны быть добавлены:

| Secret                    | Назначение                                |
|---------------------------|-------------------------------------------|
| `SECRET_KEY`              | Django SECRET_KEY                         |
| `DB_PASSWORD`             | Пароль PostgreSQL                         |
| `BASE_SERVER_URL`         | Домен или IP сервера                      |
| `DOCKER_HUB_USERNAME`     | Docker Hub username                       |
| `DOCKER_HUB_ACCESS_TOKEN` | Docker Hub access token                   |
| `SSH_KEY`                 | Приватный SSH-ключ                        |
| `SSH_USER`                | Пользователь сервера                      |
| `SERVER_IP`               | IP сервера                                |

### CI/CD (GitHub Actions)

Workflow расположен в .github/workflows/ci_cd.yaml

**Алгоритм workflow:**

1. Lint

2. Tests

3. Docker build

4. Push to Docker Hub

5. Deploy to server

Pre-commit с линтерами запускается при каждом commit.

Workflow запускается автоматически при каждом push.

### Деплой приложения

Деплой происходит автоматически после успешного прохождения тестов.

Ручной деплой на сервере:
````
cd ~/electronet
docker compose pull
docker compose up -d
````

## Принятые архитектурные решения

1. Иерархия реализована через self-relation (ForeignKey("self"))

Позволяет гибко строить структуру сети и легко масштабируется.

2. Уровень (level) вычисляется автоматически

Исключает логические ошибки и гарантирует целостность иерархии в соответствии с ТЗ.

3. Поле debt сделано read-only в API

Финансовые данные защищены от изменения через публичный интерфейс. 

Управление задолженностью осуществляется через админ-панель или бизнес-логику.

4. Разделены List и Detail сериализаторы

Оптимизация API: краткие данные в list, расширенные — в detail endpoint.

5. Контактные данные вынесены в отдельную модель Address

Структурировано и подходит для возможного масштабирования.

6. Доступ к API ограничен активными сотрудниками

Соблюдается принцип минимальных привилегий.

7. Админ-панель используется для управленческих операций

Фильтрация, ссылка на поставщика и admin action для очистки задолженности реализованы в соответствии с ТЗ.


### Автор
Надежда Попова

Python Developer

📧 nadezhdapopova13@yandex.ru

🔗 GitHub: nadezhdapopova-spec
