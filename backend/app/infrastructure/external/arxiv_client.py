"""Клиент для работы с arXiv API."""
import re
import asyncio
from typing import List, Optional

import arxiv

from app.application.dto.article_dto import ArticleSearchResultDTO


class ArxivClient:
    """Клиент для поиска и получения информации о статьях из arXiv."""

    def __init__(self):
        self._client = arxiv.Client()

    def _search_sync(
        self, query: str, max_results: int, sort_by: str
    ) -> List[ArticleSearchResultDTO]:
        sort_criterion = arxiv.SortCriterion.Relevance
        if sort_by == "submittedDate":
            sort_criterion = arxiv.SortCriterion.SubmittedDate
        elif sort_by == "lastUpdatedDate":
            sort_criterion = arxiv.SortCriterion.LastUpdatedDate

        search = arxiv.Search(
            query=query, max_results=max_results, sort_by=sort_criterion
        )

        results = []
        for paper in self._client.results(search):
            raw_id = paper.get_short_id()
            clean_id = re.sub(r"v\d+$", "", raw_id)
            results.append(
                ArticleSearchResultDTO(
                    arxiv_id=clean_id,
                    title=paper.title,
                    authors=[a.name for a in paper.authors],
                    abstract=paper.summary,
                    published_date=paper.published,
                    categories=paper.categories,
                    pdf_url=paper.pdf_url,
                    tex_url=f"https://arxiv.org/e-print/{clean_id}",
                )
            )
        return results

    async def search_articles(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
    ) -> List[ArticleSearchResultDTO]:
        """Поиск статей по запросу."""
        return await asyncio.to_thread(self._search_sync, query, max_results, sort_by)

    def _get_by_id_sync(self, arxiv_id: str) -> Optional[ArticleSearchResultDTO]:
        clean_id = re.sub(r"v\d+$", "", arxiv_id.strip())
        search = arxiv.Search(id_list=[clean_id])
        try:
            paper = next(self._client.results(search))
        except StopIteration:
            return None

        return ArticleSearchResultDTO(
            arxiv_id=clean_id,
            title=paper.title,
            authors=[a.name for a in paper.authors],
            abstract=paper.summary,
            published_date=paper.published,
            categories=paper.categories,
            pdf_url=paper.pdf_url,
            tex_url=f"https://arxiv.org/e-print/{clean_id}",
        )

    async def get_article_by_id(
        self, arxiv_id: str
    ) -> Optional[ArticleSearchResultDTO]:
        """Получить статью по arXiv ID."""
        return await asyncio.to_thread(self._get_by_id_sync, arxiv_id)
