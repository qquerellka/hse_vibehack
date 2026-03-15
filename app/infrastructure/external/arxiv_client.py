"""
МОК клиента для работы с arXiv API.

⚠️ ВНИМАНИЕ: ЭТО МОК (ЗАГЛУШКА) ⚠️

Реальная реализация поиска статей будет подключена другим разработчиком.
Этот класс возвращает тестовые данные для разработки API endpoints.

Для подключения реальной реализации:
1. Замените методы search_articles() и get_article_by_id() на реальные вызовы arXiv API
2. Используйте реальный парсинг XML ответов от arXiv
3. Обновите dependency injection в app/presentation/dependencies.py
"""
from typing import List, Optional
from datetime import datetime
from app.application.dto.article_dto import ArticleSearchResultDTO


class ArxivClient:
    """
    МОК клиента для поиска и получения информации о статьях из arXiv.
    
    ⚠️ МОК-РЕАЛИЗАЦИЯ ⚠️
    Реальная реализация будет подключена другим разработчиком.
    """
    
    async def search_articles(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "submittedDate",
        sort_order: str = "descending"
    ) -> List[ArticleSearchResultDTO]:
        """
        МОК: Поиск статей по запросу.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            query: Поисковый запрос
            max_results: Максимальное количество результатов
            sort_by: Поле для сортировки (submittedDate, relevance, lastUpdatedDate)
            sort_order: Порядок сортировки (ascending, descending)
        
        Returns:
            Список найденных статей (тестовые данные)
        
        TODO: Заменить на реальную реализацию с вызовом arXiv API
        """
        # МОК: Возвращаем тестовые данные
        return [
            ArticleSearchResultDTO(
                arxiv_id=f"2501.{10000 + i}",
                title=f"[MOCK] {query} - Test Article {i+1}",
                authors=[f"Author {i+1} A", f"Author {i+1} B"],
                abstract=f"[MOCK] This is a test abstract for article {i+1} related to '{query}'. "
                        f"This is a placeholder that will be replaced with real arXiv API calls.",
                published_date=datetime(2024, 1, 15 + i),
                categories=["cs.AI", "cs.LG"],
                pdf_url=f"https://arxiv.org/pdf/2501.{10000 + i}.pdf",
                tex_url=f"https://arxiv.org/e-print/2501.{10000 + i}"
            )
            for i in range(min(max_results, 5))  # Возвращаем максимум 5 тестовых статей
        ]
    
    async def get_article_by_id(self, arxiv_id: str) -> Optional[ArticleSearchResultDTO]:
        """
        МОК: Получить статью по arXiv ID.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            arxiv_id: ID статьи (например, "2501.12345" или "cs.AI/2501.12345")
        
        Returns:
            Информация о статье (тестовые данные) или None
        
        TODO: Заменить на реальную реализацию с вызовом arXiv API
        """
        # МОК: Возвращаем тестовые данные
        clean_id = arxiv_id.split("/")[-1] if "/" in arxiv_id else arxiv_id
        
        return ArticleSearchResultDTO(
            arxiv_id=clean_id,
            title=f"[MOCK] Test Article {clean_id}",
            authors=["Test Author 1", "Test Author 2"],
            abstract=f"[MOCK] This is a test abstract for article {clean_id}. "
                    f"This is a placeholder that will be replaced with real arXiv API call.",
            published_date=datetime(2024, 1, 15),
            categories=["cs.AI"],
            pdf_url=f"https://arxiv.org/pdf/{clean_id}.pdf",
            tex_url=f"https://arxiv.org/e-print/{clean_id}"
        )
