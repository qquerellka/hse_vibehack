# VaiBot — AI-ассистент для анализа научных статей

Мультиагентный AI-ассистент для поиска, анализа, оценки и рецензирования научных статей из arXiv. Проект создан в рамках хакатона **VibeHack 2026** для **HSE (Высшая школа экономики)**.

## Установка и запуск

### Требования
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+
- OPENROUTER_API_KEY (получить на https://openrouter.ai)

### Запуск через Docker (рекомендуется)

```bash
# 1. Клонировать
git clone <repo-url>
cd hse_vibehack

# 2. Настроить окружение
cp .env.example .env
# Добавьте OPENROUTER_API_KEY в .env

# 3. Запустить
docker-compose up --build
```

**Сервисы:**
| Сервис    | Порт  | Описание                |
|-----------|-------|-------------------------|
| Frontend  | 5173  | React SPA               |
| API       | 8000  | FastAPI backend         |
| DB        | 5433  | PostgreSQL              |
| Swagger   | 8000  | `/docs` — документация  |

### Локальный запуск

**Backend:**
```bash
cd backend
pip install -r requirements.txt
pip install -r ../agents_system/requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Основной функционал

- 🔍 **Поиск статей** — поиск по arXiv через API
- 📥 **Скачивание статей** — загрузка PDF и TeX-исходников
- 🤖 **AI-оценка** — автоматическое рецензирование: новизна, методология, влияние (1–5)
- 📝 **AI-обзор** — генерация структурированного обзора на русском языке (Executive Summary, методы, результаты, критика, вердикт)
- ❓ **Генерация тестов** — создание 5 вопросов по статье для проверки понимания
- 🖼️ **Анализ изображений** — Vision AI для описания графиков, схем и таблиц из статей
- 🔎 **Search Augmented Generation** — Tavily API для поиска дополнительного контекста

## Технологии и инструменты

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=for-the-badge&logo=typescript)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=for-the-badge&logo=langchain)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-6C5CE7?style=for-the-badge)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-06B6D4?style=for-the-badge&logo=tailwindcss)

**Ключевые библиотеки:**
- **Backend:** FastAPI, SQLAlchemy, Pydantic, LangChain, LangGraph, PyMuPDF
- **Frontend:** React 19, TanStack Query, Zustand, Axios, Radix UI, Tailwind CSS
- **Agents:** LangChain, LangGraph, Tavily, OpenRouter (GPT-4, Claude, Vision models)
- **Infra:** Docker Compose, PostgreSQL

## Команда проекта

| Участник | Роль | Контакты |
|----------|------|----------|
| **Бужор Роман** | Backend Developer | [GitHub](https://github.com/Ggh13) |
| **Крутояров Вячеслав** | Backend Developer | [GitHub](https://github.com/KrutoyarovSL) |
| **Усков Максим** | Frontend Developer | [GitHub](https://github.com/qquerellka) |
| **Мишин Илья** | AI/ML Engineer | [GitHub](https://github.com/Ippolid) |
| **Шубин Вадим** | Fullstack Developer | [GitHub](https://github.com/ghgqwer) |

## Архитектура и структура проекта

```
hse_vibehack/
├── backend/                          # FastAPI + DDD
│   └── app/
│       ├── domain/                   # Бизнес-сущности (Article, Evaluation, Review)
│       ├── application/              # Use cases + AgentService
│       ├── infrastructure/           # Database, ArxivClient, FileService
│       └── presentation/             # API endpoints, Pydantic schemas
│
├── frontend/                         # React SPA
│   └── src/
│       ├── entities/                 # API layer (article-api, session-api)
│       ├── features/                 # ArticleSearch, ArticlePicker
│       ├── widgets/                  # ArticleHub, ActivityOverview
│       └── shared/                   # UI kit, types, axios http client
│
├── agents_system/                    # AI Agents (LangGraph)
│   └── agents/
│       ├── coordinator_agent.py      # Оркестрация (маршрутизация запросов)
│       ├── describe_agent.py         # Vision AI для изображений
│       ├── review_agent.py           # Оценка статьи (EvalAgent)
│       └── writer_agent.py           # Генерация обзоров и тестов
│
└── docker-compose.yml                # Оркестрация сервисов
```

![Архитектура](https://via.placeholder.com/800x400/1a1a2e/e0e0e0?text=Architecture+Diagram)

**Поток данных:**
1. Пользователь вводит запрос → Frontend → `/api/v1/articles/search`
2. Выбирает статью → `/api/v1/articles/download` → PDF/TeX сохраняются
3. `/api/v1/evaluations/evaluate` → EvalAgent оценивает (новизна, методология, влияние)
4. `/api/v1/reviews/write` → WriterAgent генерирует обзор на русском языке

## Демонстрация работы

![Скриншот 1](https://via.placeholder.com/600x400/1a1a2e/e0e0e0?text=Screenshot+1+Search)
![Скриншот 2](https://via.placeholder.com/600x400/1a1a2e/e0e0e0?text=Screenshot+2+Evaluation)
![Скриншот 3](https://via.placeholder.com/600x400/1a1a2e/e0e0e0?text=Screenshot+3+Review)

*Скриншоты будут добавлены после деплоя.*

## Заключение

**VaiBot** — это не просто очередной поисковик статей. Это AI-first инструмент, который берёт на себя рутинную работу учёного: поиск релевантных работ, их критический анализ и структурирование выводов.

### Что отличает проект:
- **Мультиагентная архитектура** — каждый агент отвечает за свою задачу (описание изображений, оценка, написание обзора), что позволяет гибко комбинировать их для разных сценариев
- **Русскоязычные обзоры** — генерация качественных обзоров на русском языке, что особенно важно для русскоязычного научного сообщества
- **Vision AI** — анализ графиков и схем из статей, а не только текста
- **DDD архитектура** — чистый, поддерживаемый код, готовый к расширению

### Возможные улучшения:
- Поддержка других источников научных статей (PubMed, IEEE, Google Scholar)
- RAG (Retrieval-Augmented Generation) — семантический поиск по локальной коллекции статей
- История запросов и сохранение результатов в БД
- Web-интерфейс для управления агентами
- Интеграция с Notion, Obsidian для экспорта заметок

## Лицензия

Проект распространяется под лицензией **MIT**. Подробнее — в файле [LICENSE](LICENSE).
