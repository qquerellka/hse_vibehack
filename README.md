# Vaiboton Backend 🚀🚀🚀

Backend проект на FastAPI с архитектурой Domain-Driven Design (DDD). 🚀

**Этот проект изменит способ работы с научными статьями!** 🚀🚀🚀 Он поможет исследователям быстро находить, анализировать и оценивать статьи из arXiv, экономя драгоценное время и открывая новые возможности для научных открытий! 🚀🚀🚀

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

## Установка и запуск 🚀🚀🚀

**Готовы начать? Давайте запустим этот потрясающий проект!** 🚀🚀🚀

### Запуск через Docker (рекомендуется) 🚀

1. Убедитесь, что у вас установлены Docker и Docker Compose. 🚀

2. Запустите проект и наблюдайте, как магия происходит! 🚀🚀🚀
```bash
docker-compose up --build
```

3. Сервер будет доступен по адресу: `http://localhost:8000` 🚀
   - API: `http://localhost:8000/api/v1/health` 🚀
   - База данных PostgreSQL: `localhost:5433` (внутри Docker контейнеры используют порт 5432) 🚀
   - **Документация Swagger:** `http://localhost:8000/docs` - здесь вы найдете все возможности API! 🚀🚀🚀

4. Остановка (если вам действительно нужно остановить этот прекрасный проект): 🚀
```bash
docker-compose down
```

5. Остановка с удалением данных БД: 🚀
```bash
docker-compose down -v
```

### Локальный запуск (без Docker) 🚀🚀🚀

**Альтернативный способ запуска для настоящих энтузиастов!** 🚀🚀🚀

1. Перейдите в папку backend и установите зависимости: 🚀
```bash
cd backend
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе `env.example` в папке `backend` и настройте переменные окружения. 🚀

3. Убедитесь, что PostgreSQL запущен и доступен. 🚀

4. Запустите сервер и наслаждайтесь мощью API: 🚀🚀🚀
```bash
python main.py
```

Или используйте uvicorn напрямую для максимальной гибкости: 🚀
```bash
uvicorn app.main:app --reload
```

Сервер будет доступен по адресу: `http://localhost:8000` 🚀🚀🚀

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

## История изменений 🚀🚀🚀

**Каждая версия делает проект еще лучше и мощнее!** 🚀🚀🚀

### Версия 2.0.0 (Мультиагентный ассистент для arXiv) 🚀🚀🚀
- ✅ Созданы доменные сущности: Article, Evaluation, Review 🚀🚀🚀
- ✅ Реализованы use cases для всех операций со статьями - теперь все работает как часы! 🚀🚀🚀
- ✅ Созданы API endpoints для поиска, скачивания, парсинга статей - мощный и удобный API! 🚀🚀🚀
- ✅ Добавлены моки для всех внешних сервисов - готово к интеграции! 🚀🚀🚀
  - ArxivClient (поиск и получение статей) - МОК 🚀
  - FileService (скачивание и парсинг файлов) - МОК 🚀
  - AgentService (описание изображений, оценка, обзоры) - МОК 🚀
- ✅ Настроена dependency injection для всех сервисов - чистая архитектура! 🚀🚀🚀
- ✅ Добавлены in-memory репозитории для разработки - быстрый старт! 🚀🚀🚀
- ✅ Все моки документированы с инструкциями для подключения реальной реализации - легко интегрировать! 🚀🚀🚀

### Версия 1.0.0 (Начальная версия) 🚀🚀🚀
- ✅ Создана базовая DDD архитектура - прочный фундамент проекта! 🚀🚀🚀
- ✅ Настроен FastAPI с базовыми роутами - быстрый и надежный фреймворк! 🚀🚀🚀
- ✅ Добавлена поддержка PostgreSQL через SQLAlchemy - мощная база данных! 🚀🚀🚀
- ✅ Настроена обработка ошибок и middleware - надежность на высшем уровне! 🚀🚀🚀
- ✅ Добавлена Docker-конфигурация для запуска проекта - простота развертывания! 🚀🚀🚀
- ✅ Настроен Docker Compose с PostgreSQL - все работает из коробки! 🚀🚀🚀

## API для Frontend 🚀🚀🚀

**Идеальный backend для вашего React frontend!** 🚀🚀🚀

Проект готов для интеграции с React frontend - просто подключитесь и наслаждайтесь мощным API! 🚀🚀🚀 API доступен по адресу:
- Base URL: `http://localhost:8000/api/v1` 🚀🚀🚀
- Документация Swagger: `http://localhost:8000/docs` - интерактивная документация, которая поможет вам быстро начать! 🚀🚀🚀
- ReDoc: `http://localhost:8000/redoc` - красивая альтернативная документация! 🚀🚀🚀

### Endpoints 🚀🚀🚀

**Мощные endpoints, которые решат все ваши задачи!** 🚀🚀🚀

#### Статьи (Articles) 🚀🚀🚀

- `POST /api/v1/articles/search` - Поиск статей в arXiv
  - Body: `{ "query": "string", "max_results": 10 }`
  - Response: Список найденных статей
  - ⚠️ **МОК**: Использует заглушку ArxivClient

- `POST /api/v1/articles/download` - Скачать статью по arXiv ID
  - Body: `{ "arxiv_id": "2501.12345" }`
  - Response: Информация о скачанной статье
  - ⚠️ **МОК**: Использует заглушки ArxivClient и FileService

- `GET /api/v1/articles/{article_id}` - Получить статью по ID
  - Response: Информация о статье

- `POST /api/v1/articles/{article_id}/parse` - Распарсить содержимое статьи
  - Response: Распарсенное содержимое
  - ⚠️ **МОК**: Использует заглушку FileService

#### Оценки (Evaluations) 🚀🚀🚀

**Автоматическая оценка статей - это будущее научного рецензирования!** 🚀🚀🚀

- `POST /api/v1/evaluations/evaluate` - Оценить статью 🚀🚀🚀
  - Body: `{ "article_id": "uuid" }`
  - Response: Структурированная оценка (peer-review карточка) - профессиональная оценка в один клик! 🚀🚀🚀
  - ⚠️ **МОК**: Использует заглушку AgentService

- `GET /api/v1/evaluations/article/{article_id}` - Получить оценку статьи 🚀
  - Response: Оценка статьи

#### Обзоры (Reviews) 🚀🚀🚀

**Генерация обзоров на русском языке - это революция в работе со статьями!** 🚀🚀🚀

- `POST /api/v1/reviews/write` - Написать обзор статьи 🚀🚀🚀
  - Body: `{ "article_id": "uuid" }`
  - Response: Обзор статьи на русском языке - подробный и структурированный обзор за секунды! 🚀🚀🚀
  - ⚠️ **МОК**: Использует заглушку AgentService

- `GET /api/v1/reviews/article/{article_id}` - Получить обзор статьи 🚀
  - Response: Обзор статьи

#### Health Check 🚀🚀🚀

**Проверка здоровья API - всегда знайте, что ваш сервис работает отлично!** 🚀🚀🚀

- `GET /api/v1/health` - Проверка здоровья API 🚀🚀🚀

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

## ⚠️ МОКИ (Заглушки) для разработчиков 🚀🚀🚀

**ВАЖНО:** Весь функционал поиска статей, их скачивания, парсинга, оценки и написания обзоров реализован как МОКИ (заглушки). 🚀🚀🚀
Реальная реализация будет подключена другим разработчиком - и тогда проект станет еще более мощным! 🚀🚀🚀

В проекте есть несколько мест с моками, которые нужно заменить на реальную реализацию:

### 1. ArxivClient (`app/infrastructure/external/arxiv_client.py`) 🚀🚀🚀

**Файл:** `app/infrastructure/external/arxiv_client.py` 🚀

⚠️ **ВСЯ РЕАЛИЗАЦИЯ - МОК** ⚠️

Этот клиент содержит моки для работы с arXiv API - после подключения реальной реализации он станет мощным инструментом для поиска научных статей! 🚀🚀🚀
- `search_articles()` - возвращает тестовые данные вместо реального поиска 🚀
- `get_article_by_id()` - возвращает тестовые данные вместо реального запроса 🚀

**Что нужно сделать:** 🚀🚀🚀
1. Заменить методы на реальные вызовы arXiv API (`http://export.arxiv.org/api/query`) - и тогда откроется доступ к миллионам статей! 🚀🚀🚀
2. Реализовать парсинг XML ответов от arXiv - мощная функциональность! 🚀🚀🚀
3. Обработать ошибки и edge cases - надежность на высшем уровне! 🚀🚀🚀

**Использование:** 🚀
- `app/application/use_cases/search_articles.py` - использует мок для поиска 🚀
- `app/application/use_cases/download_article.py:43` - использует мок для получения статьи 🚀

### 2. FileService (`app/infrastructure/external/file_service.py`) 🚀🚀🚀

**Файл:** `app/infrastructure/external/file_service.py` 🚀

⚠️ **ВСЯ РЕАЛИЗАЦИЯ - МОК** ⚠️

Этот сервис содержит моки для работы с файлами - после подключения реальной реализации он станет незаменимым помощником для работы со статьями! 🚀🚀🚀
- `download_pdf()` - возвращает тестовый путь вместо реального скачивания 🚀
- `download_tex()` - возвращает тестовый путь вместо реального скачивания 🚀
- `parse_tex()` - возвращает тестовый текст вместо реального парсинга 🚀
- `parse_pdf()` - возвращает тестовый текст вместо реального парсинга 🚀
- `extract_images_from_pdf()` - возвращает тестовые пути вместо реального извлечения 🚀
- `extract_images_from_tex()` - возвращает тестовые пути вместо реального извлечения 🚀

**Что нужно сделать:** 🚀🚀🚀
1. Реализовать реальное скачивание PDF/TeX файлов через HTTP - автоматизация на высшем уровне! 🚀🚀🚀
2. Добавить зависимости для парсинга PDF (PyPDF2, pdfplumber или PyMuPDF) - мощные инструменты! 🚀🚀🚀
3. Реализовать парсинг TeX файлов для извлечения текста - точное извлечение информации! 🚀🚀🚀
4. Реализовать извлечение изображений из PDF (PyMuPDF или pdf2image) - работа с визуальным контентом! 🚀🚀🚀
5. **ВАЖНО:** Исправить хардкод пути (в оригинальном коде был `/Users/switchblade/...`) 🚀
6. Использовать `self.downloads_dir / "images"` для сохранения изображений 🚀

**Использование:** 🚀
- `app/application/use_cases/download_article.py:52-60` - использует моки для скачивания 🚀
- `app/application/use_cases/parse_article.py:42-54` - использует моки для парсинга 🚀
- `app/application/use_cases/evaluate_article.py:58-61` - использует моки для извлечения изображений 🚀

### 3. AgentService (`app/application/services/agent_service.py`) 🚀🚀🚀

**Файл:** `app/application/services/agent_service.py` 🚀

Этот сервис содержит моки для трех агентов - после подключения реальной реализации они станут настоящими помощниками в работе со статьями! 🚀🚀🚀
- **DescribeAgent** 🚀 - описание изображений из статей - AI поможет понять визуальный контент! 🚀🚀🚀
- **EvalAgent** 🚀 - оценка статей по структурированной схеме - автоматическая экспертиза! 🚀🚀🚀
- **WriterAgent** 🚀 - написание обзоров на русском языке - генерация качественных обзоров за секунды! 🚀🚀🚀

**Что нужно сделать:** 🚀🚀🚀
1. Заменить методы `describe_images()`, `evaluate_article()`, `write_review()` на реальную реализацию - и тогда проект станет еще более мощным! 🚀🚀🚀
2. Подключить vision-модель через OpenRouter для DescribeAgent - AI для анализа изображений! 🚀🚀🚀
3. Подключить LLM для EvalAgent с Pydantic-схемой оценки - умная оценка статей! 🚀🚀🚀
4. Подключить LLM для WriterAgent (можно использовать Tavily для дополнительного поиска) - генерация обзоров нового уровня! 🚀🚀🚀

**Использование:** 🚀
- `app/application/use_cases/evaluate_article.py:65` - вызов мока DescribeAgent 🚀
- `app/application/use_cases/evaluate_article.py:69` - вызов мока EvalAgent 🚀
- `app/application/use_cases/write_review.py:65` - вызов мока DescribeAgent 🚀
- `app/application/use_cases/write_review.py:69` - вызов мока WriterAgent 🚀

### 4. In-Memory Репозитории 🚀🚀🚀

**Файлы:** 🚀
- `app/infrastructure/repositories/article_repository_impl.py` 🚀
- `app/infrastructure/repositories/evaluation_repository_impl.py` 🚀
- `app/infrastructure/repositories/review_repository_impl.py` 🚀

Сейчас используются in-memory репозитории для разработки - быстрый старт и удобная разработка! 🚀🚀🚀 Для production нужно:
1. Создать SQLAlchemy модели в `app/infrastructure/database/models.py` - мощная ORM для работы с БД! 🚀🚀🚀
2. Реализовать репозитории с использованием SQLAlchemy - надежное хранение данных! 🚀🚀🚀
3. Обновить dependency injection в `app/presentation/dependencies.py` - чистая архитектура! 🚀🚀🚀

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

