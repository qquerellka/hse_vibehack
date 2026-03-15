"""Dependency injection для FastAPI."""
from app.domain.repositories.article_repository import ArticleRepository
from app.domain.repositories.evaluation_repository import EvaluationRepository
from app.domain.repositories.review_repository import ReviewRepository
from app.infrastructure.repositories import (
    InMemoryArticleRepository,
    InMemoryEvaluationRepository,
    InMemoryReviewRepository
)
from app.infrastructure.external import ArxivClient, FileService
from app.application.services.agent_service import AgentService


# Создаем singleton экземпляры
_article_repository: ArticleRepository = InMemoryArticleRepository()
_evaluation_repository: EvaluationRepository = InMemoryEvaluationRepository()
_review_repository: ReviewRepository = InMemoryReviewRepository()
_arxiv_client = ArxivClient()
_file_service = FileService()
_agent_service = AgentService()


def get_article_repository() -> ArticleRepository:
    """Получить репозиторий статей."""
    return _article_repository


def get_evaluation_repository() -> EvaluationRepository:
    """Получить репозиторий оценок."""
    return _evaluation_repository


def get_review_repository() -> ReviewRepository:
    """Получить репозиторий обзоров."""
    return _review_repository


def get_arxiv_client() -> ArxivClient:
    """Получить клиент arXiv."""
    return _arxiv_client


def get_file_service() -> FileService:
    """Получить сервис для работы с файлами."""
    return _file_service


def get_agent_service() -> AgentService:
    """Получить сервис агентов."""
    return _agent_service

