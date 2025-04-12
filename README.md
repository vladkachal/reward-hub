# RewardHub

> Центр управления наградами


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
