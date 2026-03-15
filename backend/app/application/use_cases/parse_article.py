"""
Use case для парсинга статьи.

⚠️ ВНИМАНИЕ: Использует МОК FileService ⚠️
Реальная реализация парсинга будет подключена другим разработчиком.
"""
from uuid import UUID
from app.domain.repositories.article_repository import ArticleRepository
from app.infrastructure.external.file_service import FileService
from app.shared.exceptions.base import NotFoundError


class ParseArticleUseCase:
    """
    Use case для парсинга содержимого статьи.
    
    ⚠️ ВНИМАНИЕ: Использует МОК FileService ⚠️
    Реальная реализация парсинга будет подключена другим разработчиком.
    """
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        file_service: FileService
    ):
        self.article_repository = article_repository
        self.file_service = file_service
    
    async def execute(self, article_id: UUID) -> str:
        """
        Распарсить содержимое статьи.
        
        Args:
            article_id: ID статьи
        
        Returns:
            Распарсенное содержимое
        
        Raises:
            NotFoundError: Если статья не найдена
        """
        article = await self.article_repository.get_by_id(article_id)
        if not article:
            raise NotFoundError(f"Article with ID {article_id} not found")
        
        # Если уже распарсено, возвращаем
        if article.parsed_content:
            return article.parsed_content
        
        # Парсим TeX если есть
        if article.local_tex_path:
            parsed = await self.file_service.parse_tex(article.local_tex_path)
            if parsed:
                article.parsed_content = parsed
                await self.article_repository.update(article)
                return parsed
        
        # Парсим PDF если есть
        if article.local_pdf_path:
            parsed = await self.file_service.parse_pdf(article.local_pdf_path)
            if parsed:
                article.parsed_content = parsed
                await self.article_repository.update(article)
                return parsed
        
        return ""

