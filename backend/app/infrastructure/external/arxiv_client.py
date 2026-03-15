"""Клиент для работы с arXiv API."""
import asyncio
from typing import List, Optional

import arxiv

from app.application.dto.article_dto import ArticleSearchResultDTO


class ArxivClient:
    """Клиент для поиска и получения информации о статьях из arXiv."""

    def __init__(self) -> None:
        self.client = arxiv.Client()

    @staticmethod
    def _map_result(paper: arxiv.Result) -> ArticleSearchResultDTO:
        clean_id = paper.get_short_id().split("v")[0]
        return ArticleSearchResultDTO(
            arxiv_id=clean_id,
            title=paper.title.strip(),
            authors=[author.name for author in paper.authors],
            abstract=paper.summary.replace("\n", " ").strip(),
            published_date=paper.published,
            categories=list(paper.categories),
            pdf_url=paper.pdf_url,
            tex_url=f"https://arxiv.org/e-print/{clean_id}",
        )

    async def search_articles(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
    ) -> List[ArticleSearchResultDTO]:
        """Поиск статей по запросу."""
        sort_criterion = {
            "submittedDate": arxiv.SortCriterion.SubmittedDate,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
            "relevance": arxiv.SortCriterion.Relevance,
        }.get(sort_by, arxiv.SortCriterion.SubmittedDate)
        sort_direction = arxiv.SortOrder.Ascending if sort_order == "ascending" else arxiv.SortOrder.Descending

        def _search() -> List[ArticleSearchResultDTO]:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=sort_criterion,
                sort_order=sort_direction,
            )
            return [self._map_result(paper) for paper in self.client.results(search)]

        return await asyncio.to_thread(_search)

    async def get_article_by_id(self, arxiv_id: str) -> Optional[ArticleSearchResultDTO]:
        """Получить статью по arXiv ID."""
        clean_id = arxiv_id.split("/")[-1]

        def _get() -> Optional[ArticleSearchResultDTO]:
            search = arxiv.Search(id_list=[clean_id])
            try:
                paper = next(self.client.results(search))
            except StopIteration:
                return None
            return self._map_result(paper)

        return await asyncio.to_thread(_get)
