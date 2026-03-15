"""
Use case для поиска статей.

⚠️ ВНИМАНИЕ: Использует МОК ArxivClient ⚠️
Реальная реализация поиска будет подключена другим разработчиком.
"""
from typing import List
from app.application.dto.article_dto import ArticleSearchResultDTO
from app.infrastructure.external.arxiv_client import ArxivClient


class SearchArticlesUseCase:
    """
    Use case для поиска статей в arXiv.
    
    ⚠️ ВНИМАНИЕ: Использует МОК ArxivClient ⚠️
    Реальная реализация поиска будет подключена другим разработчиком.
    """
    
    def __init__(self, arxiv_client: ArxivClient):
        self.arxiv_client = arxiv_client
    
    async def execute(
        self,
        query: str,
        max_results: int = 10
    ) -> List[ArticleSearchResultDTO]:
        """
        Выполнить поиск статей.
        
        Args:
            query: Поисковый запрос
            max_results: Максимальное количество результатов
        
        Returns:
            Список найденных статей
        """
        return await self.arxiv_client.search_articles(query, max_results)

