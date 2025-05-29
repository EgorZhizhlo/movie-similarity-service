```markdown
# Сервис поиска похожих отзывов

Сервис реализует семантический поиск по отзывам на фильмы с использованием дообученной модели DistilBERT, хранения эмбеддингов в PostgreSQL (+ pgvector) и асинхронной обработки через Celery + Redis.  
Написан на FastAPI, SQLAlchemy 2.0 (async) и PyTorch (CPU) + Transformers.

---

## 📁 Структура проекта

```

movie-similarity-service/
* .env                  # переменные окружения
* docker-compose.yml    # сборка контейнеров
* Dockerfile            # образ для web и worker
* requirements.txt      # зависимости Python
- app/
  * config.py             # загрузка .env
  * schemas.py            # Pydantic формы
  * main.py               # FastAPI-приложение
  * models.py             # Async SQLAlchemy + pgvector
  * services/
    - reviews.py        # DAL: save\_review, find\_similar
  * tasks.py              # Celery-таска find\_similar\_reviews
  * ml/
    - embedder.py           # обёртка DistilBERT для инференса
    - train.py              # скрипт дообучения на IMDB (опционально)
```

---

## ⚙️ Переменные окружения

Скопируйте в `.env` и заполните:

```dotenv
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=reviews
DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/reviews
CELERY_BROKER_URL=redis://redis:6379/0
````

---

## 🐳 Запуск через Docker-Compose

```bash
docker-compose up --build
```

* Контейнер `postgres` на базе образа с pgvector
* `redis` для брокера и backend Celery
* `web` (FastAPI + Uvicorn) на порту 8000
* `worker` (Celery-воркер)

После старта контейнеров веб-приложение создаст расширение `vector` и таблицу `movie_reviews`.

---

## 🚀 REST API

### 1. Добавить отзыв

**POST** `/add_review`
**Body** (JSON):

```json
{
  "text": "Ваш текст отзыва",
  "sentiment": 1
}
```

**Ответ**:

```json
{ "id": 42 }
```

### 2. Найти похожие

**POST** `/find_similar`
**Body** (JSON):

```json
{
  "text": "Текст для поиска похожих отзывов",
  "sentiment": 0
}
```

**Ответ** (сразу):

```json
{ "task_id": "abc123-..." }
```

### 3. Статус таски / результат

**GET** `/status/{task_id}`
**Ответы**:

* **PENDING** (в очереди или на обработке):

  ```json
  { "status": "PENDING" }
  ```
* **SUCCESS** (успешно):

  ```json
  {
    "status": "SUCCESS",
    "similar": [
      "Первый похожий отзыв",
      "Второй похожий отзыв",
      "Третий похожий отзыв"
    ]
  }
  ```
* **FAILURE** (ошибка):

  ```json
  {
    "status": "FAILURE",
    "info": "<текст ошибки>"
  }
  ```

---

## 📊 Пример тестовых данных

```json
  {"text":"I absolutely loved this movie, it was fantastic!","sentiment":1}
```
```json
  {"text":"The film was a dull and boring experience.","sentiment":0}
```
```json
  {"text":"An average movie with some good moments.","sentiment":0}
```
```json
  {"text":"A masterpiece of cinematography and storytelling.","sentiment":1}
```

1. Добавьте их через `/add_review`.
2. Запустите поиск:

   ```bash
   curl -X POST http://localhost:8000/find_similar \
     -H "Content-Type: application/json" \
     -d '{"text":"What a wonderful film with stunning visuals","sentiment":1}'
   ```
3. Поставьте `/status/{task_id}` — получите 3 самых близких отзыва того же `sentiment`.

---

## ✅ Критерии готовности

* ✅ FastAPI + Pydantic
* ✅ Async SQLAlchemy + pgvector
* ✅ Redis + Celery (broker+backend)
* ✅ PyTorch (CPU) + Transformers (DistilBERT)
* ✅ REST API `/add_review`, `/find_similar`, `/status/{task_id}`

---

