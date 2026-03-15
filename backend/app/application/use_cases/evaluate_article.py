"""Use case для оценки статьи."""
from uuid import UUID
from app.domain.repositories.article_repository import ArticleRepository
from app.domain.repositories.evaluation_repository import EvaluationRepository
from app.application.services.agent_service import AgentService
from app.infrastructure.external.file_service import FileService
from app.application.dto.evaluation_dto import EvaluationDTO
from app.application.dto.mappers import evaluation_to_dto
from app.shared.exceptions.base import NotFoundError


class EvaluateArticleUseCase:
    """
    Use case для оценки статьи.
    
    Использует AgentService (МОК) для генерации оценки.
    """
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        evaluation_repository: EvaluationRepository,
        agent_service: AgentService,
        file_service: FileService
    ):
        self.article_repository = article_repository
        self.evaluation_repository = evaluation_repository
        self.agent_service = agent_service
        self.file_service = file_service
    
    async def execute(self, article_id: UUID) -> EvaluationDTO:
        """
        Оценить статью.
        
        Args:
            article_id: ID статьи
        
        Returns:
            Структурированная оценка
        
        Raises:
            NotFoundError: Если статья не найдена
        """
        # Проверяем, есть ли уже оценка
        existing_evaluation = await self.evaluation_repository.get_by_article_id(article_id)
        if existing_evaluation:
            return evaluation_to_dto(existing_evaluation)
        
        # Получаем статью
        article = await self.article_repository.get_by_id(article_id)
        if not article:
            raise NotFoundError(f"Article with ID {article_id} not found")
        
        if not article.parsed_content:
            if article.local_tex_path:
                article.parsed_content = await self.file_service.parse_tex(article.local_tex_path)
            elif article.local_pdf_path:
                article.parsed_content = await self.file_service.parse_pdf(article.local_pdf_path)
            if article.parsed_content:
                await self.article_repository.update(article)

        article_content = article.parsed_content or article.abstract
        
        # Извлекаем изображения
        image_paths = []
        if article.local_pdf_path:
            image_paths = await self.file_service.extract_images_from_pdf(article.local_pdf_path)
        elif article.local_tex_path:
            image_paths = await self.file_service.extract_images_from_tex(article.local_tex_path)
        
        image_descriptions = await self.agent_service.describe_images(image_paths)
        
        evaluation_dto = await self.agent_service.evaluate_article(
            article_id,
            article_content,
            image_descriptions
        )
        
        # Сохраняем оценку в БД
        from app.domain.entities.evaluation import Evaluation
        evaluation = Evaluation(
            article_id=evaluation_dto.article_id,
            category=evaluation_dto.category,
            relevance=evaluation_dto.relevance,
            novelty_score=evaluation_dto.novelty_score,
            methodology_score=evaluation_dto.methodology_score,
            impact_score=evaluation_dto.impact_score,
            overall_score=evaluation_dto.overall_score,
            pros=evaluation_dto.pros,
            cons=evaluation_dto.cons,
            justification=evaluation_dto.justification
        )
        
        saved_evaluation = await self.evaluation_repository.create(evaluation)
        return evaluation_to_dto(saved_evaluation)
