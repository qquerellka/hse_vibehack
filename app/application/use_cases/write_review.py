"""Use case для написания обзора статьи."""
from uuid import UUID
from app.domain.repositories.article_repository import ArticleRepository
from app.domain.repositories.review_repository import ReviewRepository
from app.application.services.agent_service import AgentService
from app.infrastructure.external.file_service import FileService
from app.application.dto.review_dto import ReviewDTO
from app.application.dto.mappers import review_to_dto
from app.shared.exceptions.base import NotFoundError


class WriteReviewUseCase:
    """
    Use case для написания обзора статьи.
    
    Использует AgentService (МОК) для генерации обзора.
    """
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        review_repository: ReviewRepository,
        agent_service: AgentService,
        file_service: FileService
    ):
        self.article_repository = article_repository
        self.review_repository = review_repository
        self.agent_service = agent_service
        self.file_service = file_service
    
    async def execute(self, article_id: UUID) -> ReviewDTO:
        """
        Написать обзор статьи.
        
        Args:
            article_id: ID статьи
        
        Returns:
            Обзор статьи на русском языке
        
        Raises:
            NotFoundError: Если статья не найдена
        """
        # Проверяем, есть ли уже обзор
        existing_review = await self.review_repository.get_by_article_id(article_id)
        if existing_review:
            return review_to_dto(existing_review)
        
        # Получаем статью
        article = await self.article_repository.get_by_id(article_id)
        if not article:
            raise NotFoundError(f"Article with ID {article_id} not found")
        
        # Получаем содержимое статьи
        article_content = article.parsed_content or article.abstract
        
        # Извлекаем изображения
        image_paths = []
        if article.local_pdf_path:
            image_paths = await self.file_service.extract_images_from_pdf(article.local_pdf_path)
        elif article.local_tex_path:
            image_paths = await self.file_service.extract_images_from_tex(article.local_tex_path)
        
        # ⚠️ МОК: Описываем изображения через AgentService
        # TODO: Заменить на реальный DescribeAgent
        image_descriptions = await self.agent_service.describe_images(image_paths)
        
        # ⚠️ МОК: Пишем обзор через AgentService
        # TODO: Заменить на реальный WriterAgent
        review_dto = await self.agent_service.write_review(
            article_id,
            article_content,
            image_descriptions
        )
        
        # Сохраняем обзор в БД
        from app.domain.entities.review import Review
        review = Review(
            article_id=review_dto.article_id,
            summary=review_dto.summary,
            methods=review_dto.methods,
            results=review_dto.results,
            criticism=review_dto.criticism,
            application=review_dto.application,
            verdict=review_dto.verdict,
            full_text=review_dto.full_text
        )
        
        saved_review = await self.review_repository.create(review)
        return review_to_dto(saved_review)

