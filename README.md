# RewardHub

> Центр управления наградами

Это backend-приложение представляет собой API-платформу для управления системой
наград пользователей. Основной функционал включает:

- **Аутентификация и авторизация** с использованием JWT-токенов (получение,
  обновление, валидация токенов), с настройкой CORS для доступа с фронтенда
  (например, localhost:3000).
- **Система отложенных наград**, реализованная через Celery и Redis. Награды
  начисляются не мгновенно, а через заданное время (execute_at), что позволяет
  гибко планировать выдачу бонусов.
- **Возможность ручного запроса награды** пользователями через отдельную
  конечную точку /api/rewards/request/, с ограничением: не чаще одного
  раза в сутки. При успешном запросе создаётся отложенная награда
  в размере 10 монет, которая будет выдана через 5 минут.
- **Логирование наград** — каждая выданная награда фиксируется
  в модели RewardLog, что позволяет отслеживать историю начислений пользователю.
- **Гибкое разделение типов наград** — реализовано через отдельную модель,
  связанную по one-to-one с отложенной наградой, что позволяет отделить вручную
  запрошенные награды от автоматически созданных.
- **Полная OpenAPI-документация** с использованием drf-spectacular, включая
  аннотации, описания и резюме для всех конечных точек.
- **Чистая архитектура:** логика разделена по слоям, используются менеджеры и
  кастомные QuerySet-классы для инкапсуляции бизнес-правил. Такой подход
  повышает читаемость и расширяемость кода.

## Предварительные требования

Перед началом работы убедитесь, что у вас установлены следующие компоненты:

- Docker версии 4.22 или выше
- Docker Compose версии 2.20 или выше


## Начало работы

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/vladkachal/reward-hub.git
cd reward-hub
```

### 2. Настройте переменные окружения

Скопируйте файл `.env.template` в `.env`.
Редактируйте файл .env.
Следующие переменные окружения обязательны для заполнения:

- DEBUG=True (так как это тестовое приложение)
- SECRET_KEY=
- ALLOWED_HOSTS=localhost,127.0.0.1
- DATABASE_PASSWORD=

### 3. Соберите и запустите приложение

Используйте Docker Compose для сборки и запуска приложения:

```bash
export COMPOSE_FILE=./docker/compose.development.yaml
docker compose up --build
```

### 4. Создайте суперпользователя:

Чтобы получить доступ к панели администратора Django,
создайте суперпользователя:

```bash
docker compose exec django python src/manage.py createsuperuser
```

### 5. Доступ к приложению:

- Панель администратора Django: http://localhost:8000/admin/
- Документация API: http://localhost:8000/api/docs/ (доступ разрешен только
  для суперпользователей)


## Комментарии к проекту

Поскольку это тестовый проект, я намеренно упростил некоторые части
стартового шаблона, чтобы не перегружать кодовую базу. Были удалены некоторые
комментарии и часть документации.

**Ниже — практики и инструменты, которые я обычно использую** при запуске нового
проекта или при рефакторинге существующего, если поставлена такая задача:

### Docker

- Создание отдельного пользователя внутри контейнера без прав `root`.
- Использование более профессиональной конфигурации с `nginx` + `uvicorn`
  для продакшн-развертывания.

### Django

- Гибкая система `settings.py`, адаптированная под разные окружения: development,
  staging, production, testing.
- Вместо `UUID` для поля `id` используется уникальный идентификатор `NanoID`
  — это обеспечивает не только безопасность и непредсказуемость URL-ов,
  но еще и удобочитаемость.
- Для авторизации используется библиотека `django-allauth`, обеспечивающая
  расширяемую и стабильную систему аутентификации.
- Пароли хэшируются с использованием алгоритма `argon2`, как одного из самых
  безопасных по состоянию на сегодня.
- Включена Content Security Policy (CSP) для повышения безопасности
  административной панели.
- Rate limiting — ограничение частоты запросов для защиты от злоупотреблений.
- Иерархическая структура OpenAPI-документации с использованием Swagger UI,
  обеспечивающая удобную навигацию и поддержку масштабируемости.

### Очереди (Celery)

В этом проекте используется `Redis` как брокер задач, однако
для продакшн-сценариев предпочтительнее использовать `RabbitMQ`, который имеет
поддержку очередей с подтверждением доставки и лучше работает
с сохранением данных.
