"""
Use case для скачивания статьи.

⚠️ ВНИМАНИЕ: Использует МОКИ ArxivClient и FileService ⚠️
Реальная реализация будет подключена другим разработчиком.
"""
from typing import Optional
from uuid import UUID
from app.domain.entities.article import Article
from app.domain.repositories.article_repository import ArticleRepository
from app.infrastructure.external.arxiv_client import ArxivClient
from app.infrastructure.external.file_service import FileService
from app.shared.exceptions.base import NotFoundError


class DownloadArticleUseCase:
    """
    Use case для скачивания статьи.
    
    ⚠️ ВНИМАНИЕ: Использует МОКИ ArxivClient и FileService ⚠️
    Реальная реализация будет подключена другим разработчиком.
    """
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        arxiv_client: ArxivClient,
        file_service: FileService
    ):
        self.article_repository = article_repository
        self.arxiv_client = arxiv_client
        self.file_service = file_service
    
    async def execute(self, arxiv_id: str) -> Article:
        """
        Скачать статью по arXiv ID.
        
        Args:
            arxiv_id: arXiv ID статьи
        
        Returns:
            Сохраненная статья
        
        Raises:
            NotFoundError: Если статья не найдена
        """
        # Проверяем, есть ли статья уже в БД
        existing_article = await self.article_repository.get_by_arxiv_id(arxiv_id)
        if existing_article:
            return existing_article
        
        # Получаем информацию о статье из arXiv
        article_info = await self.arxiv_client.get_article_by_id(arxiv_id)
        if not article_info:
            raise NotFoundError(f"Article with arXiv ID {arxiv_id} not found")
        
        # Скачиваем файлы
        pdf_path = None
        tex_path = None
        
        if article_info.pdf_url:
            pdf_path = await self.file_service.download_pdf(
                article_info.pdf_url,
                arxiv_id
            )
        
        if article_info.tex_url:
            tex_path = await self.file_service.download_tex(
                article_info.tex_url,
                arxiv_id
            )
        
        # Создаем доменную сущность
        article = Article(
            arxiv_id=article_info.arxiv_id,
            title=article_info.title,
            authors=article_info.authors,
            abstract=article_info.abstract,
            published_date=article_info.published_date,
            categories=article_info.categories or [],
            pdf_url=article_info.pdf_url,
            tex_url=article_info.tex_url,
            local_pdf_path=pdf_path,
            local_tex_path=tex_path
        )
        
        # Сохраняем в БД
        return await self.article_repository.create(article)

