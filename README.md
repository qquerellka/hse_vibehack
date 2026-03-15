# Vaiboton Backend

Backend проект на FastAPI с архитектурой Domain-Driven Design (DDD).

## Структура проекта

```
hse_vibehack/
├── app/
│   ├── domain/                    # Доменный слой (бизнес-логика)
│   │   ├── entities/             # Доменные сущности
│   │   ├── repositories/         # Интерфейсы репозиториев
│   │   └── value_objects/        # Value Objects
│   │
│   ├── application/              # Слой приложения
│   │   ├── use_cases/           # Use Cases (бизнес-сценарии)
│   │   ├── dto/                 # Data Transfer Objects
│   │   └── services/            # Сервисы приложения
│   │
│   ├── infrastructure/           # Слой инфраструктуры
│   │   ├── database/            # Настройка БД
│   │   ├── repositories/        # Реализация репозиториев
│   │   └── config/              # Конфигурация
│   │
│   ├── presentation/             # Слой представления
│   │   ├── api/                 # API роуты
│   │   │   └── v1/              # API версии 1
│   │   ├── schemas/             # Pydantic схемы
│   │   └── middleware/          # Middleware
│   │
│   ├── shared/                   # Общие компоненты
│   │   ├── exceptions/          # Исключения
│   │   └── utils/               # Утилиты
│   │
│   └── main.py                  # Главный файл приложения
│
├── main.py                       # Точка входа для запуска сервера
├── requirements.txt              # Зависимости
├── Dockerfile                    # Docker образ приложения
├── docker-compose.yml            # Docker Compose конфигурация
├── .dockerignore                 # Исключения для Docker
├── env.example                   # Пример файла с переменными окружения
└── .gitignore

```

## Установка и запуск

### Запуск через Docker (рекомендуется)

1. Убедитесь, что у вас установлены Docker и Docker Compose.

2. Запустите проект:
```bash
docker-compose up --build
```

3. Сервер будет доступен по адресу: `http://localhost:8000`
   - API: `http://localhost:8000/api/v1/health`
   - База данных PostgreSQL: `localhost:5433` (внутри Docker контейнеры используют порт 5432) 🚀
   - Документация Swagger: `http://localhost:8000/docs`

4. Остановка:
```bash
docker-compose down
```

5. Остановка с удалением данных БД:
```bash
docker-compose down -v
```

### Локальный запуск (без Docker)

1. Перейдите в папку backend и установите зависимости: 🚀
```bash
cd backend
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе `env.example` в папке `backend` и настройте переменные окружения.

3. Убедитесь, что PostgreSQL запущен и доступен.

4. Запустите сервер:
```bash
python main.py
```

Или используйте uvicorn напрямую:
```bash
uvicorn app.main:app --reload
```

## Архитектура DDD 🚀🚀🚀

**Потрясающая архитектура, которая делает этот проект масштабируемым и поддерживаемым!** 🚀🚀🚀

Проект организован по принципам Domain-Driven Design - это означает чистый код, четкое разделение ответственности и возможность легко расширять функциональность! 🚀🚀🚀

- **Domain Layer** 🚀 - содержит бизнес-логику, сущности и интерфейсы репозиториев. Это сердце проекта!
- **Application Layer** 🚀 - содержит use cases и сервисы приложения. Здесь происходит вся магия!
- **Infrastructure Layer** 🚀 - реализация технических деталей (БД, внешние сервисы). Надежная основа проекта!
- **Presentation Layer** 🚀 - API endpoints, схемы валидации, middleware. Красивый интерфейс для взаимодействия!

## Добавление нового функционала 🚀🚀🚀

**Хотите внести свой вклад в этот потрясающий проект? Отлично!** 🚀🚀🚀

При добавлении новых фич следуйте принципам DDD архитектуры - это гарантирует качество и поддерживаемость кода! 🚀🚀🚀

1. Создайте доменную сущность в `app/domain/entities/` 🚀
2. Определите интерфейс репозитория в `app/domain/repositories/` 🚀
3. Реализуйте репозиторий в `app/infrastructure/repositories/` 🚀
4. Создайте use case в `app/application/use_cases/` 🚀
5. Добавьте API endpoint в `app/presentation/api/v1/` 🚀
6. Создайте Pydantic схемы в `app/presentation/schemas/` 🚀

**Важно:** Все новые фичи должны быть задокументированы в разделе "История изменений" ниже. 🚀🚀🚀

## История изменений

### Версия 2.0.0
- Созданы доменные сущности: `Article`, `Evaluation`, `Review`
- Реализованы use cases для поиска, скачивания, парсинга, оценки и обзора статей
- Добавлены API endpoints для frontend
- Настроена dependency injection
- Добавлены in-memory репозитории для runtime-хранения данных

### Версия 1.0.0
- Создана базовая DDD-архитектура
- Настроен FastAPI
- Добавлена Docker-конфигурация

## API для Frontend

- Base URL: `http://localhost:8000/api/v1`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

- `POST /api/v1/articles/search` - поиск статей в arXiv
- `POST /api/v1/articles/download` - скачивание статьи по `arxiv_id`
- `GET /api/v1/articles/{article_id}` - получение статьи по внутреннему `UUID`
- `POST /api/v1/articles/{article_id}/parse` - парсинг содержимого статьи
- `POST /api/v1/evaluations/evaluate` - оценка статьи
- `GET /api/v1/evaluations/article/{article_id}` - получение сохраненной оценки
- `POST /api/v1/reviews/write` - написание обзора
- `GET /api/v1/reviews/article/{article_id}` - получение сохраненного обзора
- `GET /api/v1/health` - health check

### Детальное описание запросов и ответов 🚀🚀🚀

**Подробные форматы данных для каждого endpoint - все что нужно для интеграции!** 🚀🚀🚀

#### Статьи (Articles) - Форматы данных 🚀🚀🚀

##### 1. `POST /api/v1/articles/search` - Поиск статей

**Запрос (Request Body):**
```json
{
  "query": "machine learning",
  "max_results": 10
}
```

**Параметры:**
- `query` (string, обязательный) - Поисковый запрос для поиска статей в arXiv
- `max_results` (integer, опциональный, по умолчанию: 10) - Максимальное количество результатов (от 1 до 100)

**Ответ (Response) - Массив статей:**
```json
[
  {
    "id": "",
    "arxiv_id": "2501.12345",
    "title": "Example Article Title",
    "authors": ["Author One", "Author Two"],
    "abstract": "This is the abstract of the article...",
    "published_date": "2025-01-15T00:00:00",
    "categories": ["cs.AI", "cs.LG"],
    "pdf_url": "http://arxiv.org/pdf/2501.12345.pdf",
    "tex_url": "http://arxiv.org/src/2501.12345"
  }
]
```

**Поля ответа:**
- `id` (string) - UUID статьи (пустая строка для результатов поиска, т.к. статья еще не сохранена)
- `arxiv_id` (string) - arXiv ID статьи (например, "2501.12345")
- `title` (string) - Название статьи
- `authors` (array[string]) - Список авторов
- `abstract` (string) - Аннотация статьи
- `published_date` (string, nullable) - Дата публикации в формате ISO 8601
- `categories` (array[string]) - Категории arXiv (например, ["cs.AI", "cs.LG"])
- `pdf_url` (string, nullable) - URL PDF файла статьи
- `tex_url` (string, nullable) - URL TeX исходников статьи

---

##### 2. `POST /api/v1/articles/download` - Скачать статью

**Запрос (Request Body):**
```json
{
  "arxiv_id": "2501.12345"
}
```

**Параметры:**
- `arxiv_id` (string, обязательный) - arXiv ID статьи (например, "2501.12345")

**Ответ (Response):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "arxiv_id": "2501.12345",
  "title": "Example Article Title",
  "authors": ["Author One", "Author Two"],
  "abstract": "This is the abstract of the article...",
  "published_date": "2025-01-15T00:00:00",
  "categories": ["cs.AI", "cs.LG"],
  "pdf_url": "http://arxiv.org/pdf/2501.12345.pdf",
  "tex_url": "http://arxiv.org/src/2501.12345",
  "local_pdf_path": "./downloads/2501.12345.pdf",
  "local_tex_path": "./downloads/2501.12345.tex",
  "parsed_content": null
}
```

**Дополнительные поля (по сравнению с поиском):**
- `id` (string) - UUID сохраненной статьи
- `local_pdf_path` (string, nullable) - Локальный путь к скачанному PDF файлу
- `local_tex_path` (string, nullable) - Локальный путь к скачанному TeX файлу
- `parsed_content` (string, nullable) - Распарсенное содержимое статьи (если уже распарсено)

**Ошибки:**
- `404 Not Found` - Статья не найдена в arXiv

---

##### 3. `GET /api/v1/articles/{article_id}` - Получить статью по ID

**Параметры URL:**
- `article_id` (string, обязательный) - UUID статьи

**Ответ (Response):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "arxiv_id": "2501.12345",
  "title": "Example Article Title",
  "authors": ["Author One", "Author Two"],
  "abstract": "This is the abstract of the article...",
  "published_date": "2025-01-15T00:00:00",
  "categories": ["cs.AI", "cs.LG"],
  "pdf_url": "http://arxiv.org/pdf/2501.12345.pdf",
  "tex_url": "http://arxiv.org/src/2501.12345",
  "local_pdf_path": "./downloads/2501.12345.pdf",
  "local_tex_path": "./downloads/2501.12345.tex",
  "parsed_content": "Parsed content of the article..."
}
```

**Ошибки:**
- `400 Bad Request` - Неверный формат UUID
- `404 Not Found` - Статья не найдена

---

##### 4. `POST /api/v1/articles/{article_id}/parse` - Распарсить статью

**Параметры URL:**
- `article_id` (string, обязательный) - UUID статьи

**Ответ (Response):**
```json
{
  "article_id": "550e8400-e29b-41d4-a716-446655440000",
  "parsed_content": "Parsed content of the article from PDF or TeX file..."
}
```

**Поля ответа:**
- `article_id` (string) - UUID статьи
- `parsed_content` (string) - Распарсенное текстовое содержимое статьи

**Ошибки:**
- `400 Bad Request` - Неверный формат UUID
- `404 Not Found` - Статья не найдена

---

#### Оценки (Evaluations) - Форматы данных 🚀🚀🚀

##### 1. `POST /api/v1/evaluations/evaluate` - Оценить статью

**Запрос (Request Body):**
```json
{
  "article_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Параметры:**
- `article_id` (string, обязательный) - UUID статьи для оценки

**Ответ (Response):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "article_id": "550e8400-e29b-41d4-a716-446655440000",
  "category": "Machine Learning",
  "relevance": "Highly relevant to the field",
  "novelty_score": 4,
  "methodology_score": 5,
  "impact_score": 4,
  "overall_score": 4,
  "pros": [
    "Novel approach to the problem",
    "Well-structured methodology",
    "Clear experimental results"
  ],
  "cons": [
    "Limited dataset",
    "Could benefit from more comparisons"
  ],
  "justification": "This article presents a novel approach with solid methodology. The experimental results are clear, though the dataset could be expanded."
}
```

**Поля ответа:**
- `id` (string) - UUID оценки
- `article_id` (string) - UUID оцениваемой статьи
- `category` (string) - Категория оценки
- `relevance` (string) - Релевантность статьи
- `novelty_score` (integer, 1-5) - Оценка новизны (1 = низкая, 5 = высокая)
- `methodology_score` (integer, 1-5) - Оценка методологии
- `impact_score` (integer, 1-5) - Оценка влияния/важности
- `overall_score` (integer, 1-5) - Общая оценка
- `pros` (array[string]) - Список преимуществ статьи
- `cons` (array[string]) - Список недостатков статьи
- `justification` (string) - Обоснование оценки

**Ошибки:**
- `400 Bad Request` - Неверный формат UUID
- `404 Not Found` - Статья не найдена

---

##### 2. `GET /api/v1/evaluations/article/{article_id}` - Получить оценку статьи

**Параметры URL:**
- `article_id` (string, обязательный) - UUID статьи

**Ответ (Response):**
Формат такой же, как у `POST /api/v1/evaluations/evaluate`

**Ошибки:**
- `400 Bad Request` - Неверный формат UUID
- `404 Not Found` - Оценка не найдена

---

#### Обзоры (Reviews) - Форматы данных 🚀🚀🚀

##### 1. `POST /api/v1/reviews/write` - Написать обзор статьи

**Запрос (Request Body):**
```json
{
  "article_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Параметры:**
- `article_id` (string, обязательный) - UUID статьи для обзора

**Ответ (Response):**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "article_id": "550e8400-e29b-41d4-a716-446655440000",
  "summary": "В данной статье рассматривается новый подход к машинному обучению...",
  "methods": "Авторы используют метод глубокого обучения с архитектурой трансформера...",
  "results": "Экспериментальные результаты показывают улучшение точности на 15%...",
  "criticism": "Основные ограничения работы связаны с размером датасета...",
  "application": "Предложенный метод может быть применен в задачах обработки естественного языка...",
  "verdict": "Статья представляет значительный интерес для исследователей в области NLP...",
  "full_text": "# Обзор статьи\n\n## Резюме\n\nВ данной статье рассматривается...\n\n## Методы\n\n..."
}
```

**Поля ответа:**
- `id` (string) - UUID обзора
- `article_id` (string) - UUID статьи
- `summary` (string) - Резюме статьи (на русском языке)
- `methods` (string) - Описание методов, использованных в статье
- `results` (string) - Описание результатов исследования
- `criticism` (string) - Критика и ограничения работы
- `application` (string) - Области применения результатов
- `verdict` (string) - Общий вердикт и выводы
- `full_text` (string) - Полный текст обзора в формате Markdown

**Ошибки:**
- `400 Bad Request` - Неверный формат UUID
- `404 Not Found` - Статья не найдена

---

##### 2. `GET /api/v1/reviews/article/{article_id}` - Получить обзор статьи

**Параметры URL:**
- `article_id` (string, обязательный) - UUID статьи

**Ответ (Response):**
Формат такой же, как у `POST /api/v1/reviews/write`

**Ошибки:**
- `400 Bad Request` - Неверный формат UUID
- `404 Not Found` - Обзор не найден

---

#### Health Check - Формат данных 🚀🚀🚀

##### `GET /api/v1/health` - Проверка здоровья API

**Ответ (Response):**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

**Поля ответа:**
- `status` (string) - Статус API ("ok" при нормальной работе)
- `message` (string) - Сообщение о состоянии API

---

### Коды ошибок HTTP 🚀🚀🚀

**Стандартные коды ответов API:** 🚀🚀🚀

- `200 OK` - Успешный запрос
- `400 Bad Request` - Неверный формат данных в запросе (например, неверный UUID)
- `404 Not Found` - Запрашиваемый ресурс не найден (статья, оценка, обзор)
- `422 Unprocessable Entity` - Ошибка валидации данных (Pydantic)
- `500 Internal Server Error` - Внутренняя ошибка сервера

**Формат ошибки:**
```json
{
  "detail": "Описание ошибки"
}
```

## Реализации и ограничения

- Backend использует `agents_system` для поиска, скачивания, парсинга, оценки и обзора статей.
- Во frontend больше нет локальных заглушек и вызовов несуществующих `/analytics` или `/history`.
- Для хранения статей, оценок и обзоров сейчас используются in-memory репозитории.
- Для полноценного production persistence нужно добавить SQLAlchemy-модели и заменить in-memory репозитории на работу с БД.

## Структура данных 🚀🚀🚀

**Понятная и логичная структура данных - основа успешного проекта!** 🚀🚀🚀

### Article (Статья) 🚀🚀🚀

**Полная информация о научной статье - все что нужно для работы!** 🚀🚀🚀

- `id` (UUID) - Уникальный идентификатор 🚀
- `arxiv_id` (str) - arXiv ID статьи 🚀
- `title` (str) - Название 🚀
- `authors` (List[str]) - Авторы 🚀
- `abstract` (str) - Аннотация 🚀
- `published_date` (datetime) - Дата публикации 🚀
- `categories` (List[str]) - Категории 🚀
- `pdf_url` / `tex_url` - Ссылки на файлы 🚀
- `local_pdf_path` / `local_tex_path` - Локальные пути к файлам 🚀
- `parsed_content` (str) - Распарсенное содержимое 🚀

### Evaluation (Оценка) 🚀🚀🚀

**Структурированная оценка статьи - профессиональный peer-review в структурированном виде!** 🚀🚀🚀

- `id` (UUID) - Уникальный идентификатор 🚀
- `article_id` (UUID) - ID статьи 🚀
- `category` (str) - Категория 🚀
- `relevance` (str) - Релевантность 🚀
- `novelty_score` / `methodology_score` / `impact_score` / `overall_score` (int, 1-5) - Баллы 🚀🚀🚀
- `pros` / `cons` (List[str]) - Плюсы и минусы 🚀
- `justification` (str) - Обоснование 🚀

### Review (Обзор) 🚀🚀🚀

**Подробный обзор статьи на русском языке - все разделы для полного понимания!** 🚀🚀🚀

- `id` (UUID) - Уникальный идентификатор 🚀
- `article_id` (UUID) - ID статьи 🚀
- `summary` / `methods` / `results` / `criticism` / `application` / `verdict` (str) - Разделы обзора 🚀🚀🚀
- `full_text` (str) - Полный текст обзора в Markdown 🚀🚀🚀

---

**Этот проект поможет тысячам исследователей работать эффективнее!** 🚀🚀🚀 **Присоединяйтесь к революции в работе с научными статьями!** 🚀🚀🚀
