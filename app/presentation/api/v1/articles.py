"""API endpoints для работы со статьями."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.use_cases import (
    SearchArticlesUseCase,
    DownloadArticleUseCase,
    ParseArticleUseCase
)
from app.application.dto.mappers import article_to_dto
from app.infrastructure.external import ArxivClient
from app.presentation.dependencies import (
    get_article_repository,
    get_arxiv_client,
    get_file_service
)
from app.presentation.schemas import (
    SearchArticlesRequest,
    DownloadArticleRequest,
    ParseArticleRequest,
    ArticleResponse
)
from app.shared.exceptions.base import NotFoundError

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/search", response_model=list[ArticleResponse])
async def search_articles(
    request: SearchArticlesRequest,
    arxiv_client: ArxivClient = Depends(get_arxiv_client)
):
    """
    Поиск статей в arXiv.
    
    ⚠️ ВНИМАНИЕ: Использует МОК ArxivClient ⚠️
    Реальная реализация поиска будет подключена другим разработчиком.
    
    Args:
        request: Параметры поиска
        arxiv_client: Клиент arXiv (МОК)
    
    Returns:
        Список найденных статей (тестовые данные)
    """
    use_case = SearchArticlesUseCase(arxiv_client)
    results = await use_case.execute(request.query, request.max_results)
    
    return [
        ArticleResponse(
            id="",  # Статьи из поиска еще не сохранены
            arxiv_id=result.arxiv_id,
            title=result.title,
            authors=result.authors,
            abstract=result.abstract,
            published_date=result.published_date.isoformat() if result.published_date else None,
            categories=result.categories or [],
            pdf_url=result.pdf_url,
            tex_url=result.tex_url
        )
        for result in results
    ]


@router.post("/download", response_model=ArticleResponse)
async def download_article(
    request: DownloadArticleRequest,
    article_repository=Depends(get_article_repository),
    arxiv_client=Depends(get_arxiv_client),
    file_service=Depends(get_file_service)
):
    """
    Скачать статью по arXiv ID.
    
    ⚠️ ВНИМАНИЕ: Использует МОКИ ArxivClient и FileService ⚠️
    Реальная реализация будет подключена другим разработчиком.
    
    Args:
        request: Параметры скачивания
        article_repository: Репозиторий статей
        arxiv_client: Клиент arXiv (МОК)
        file_service: Сервис для работы с файлами (МОК)
    
    Returns:
        Информация о скачанной статье (тестовые данные)
    """
    use_case = DownloadArticleUseCase(article_repository, arxiv_client, file_service)
    
    try:
        article = await use_case.execute(request.arxiv_id)
        dto = article_to_dto(article)
        
        return ArticleResponse(
            id=str(dto.id),
            arxiv_id=dto.arxiv_id,
            title=dto.title,
            authors=dto.authors,
            abstract=dto.abstract,
            published_date=dto.published_date.isoformat() if dto.published_date else None,
            categories=dto.categories,
            pdf_url=dto.pdf_url,
            tex_url=dto.tex_url,
            local_pdf_path=dto.local_pdf_path,
            local_tex_path=dto.local_tex_path,
            parsed_content=dto.parsed_content
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{article_id}/parse")
async def parse_article(
    article_id: str,
    article_repository=Depends(get_article_repository),
    file_service=Depends(get_file_service)
):
    """
    Распарсить содержимое статьи.
    
    ⚠️ ВНИМАНИЕ: Использует МОК FileService ⚠️
    Реальная реализация парсинга будет подключена другим разработчиком.
    
    Args:
        article_id: UUID статьи
        article_repository: Репозиторий статей
        file_service: Сервис для работы с файлами (МОК)
    
    Returns:
        Распарсенное содержимое (тестовые данные)
    """
    try:
        article_uuid = UUID(article_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid article ID format"
        )
    
    use_case = ParseArticleUseCase(article_repository, file_service)
    
    try:
        parsed_content = await use_case.execute(article_uuid)
        return {"article_id": article_id, "parsed_content": parsed_content}
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: str,
    article_repository=Depends(get_article_repository)
):
    """
    Получить статью по ID.
    
    Args:
        article_id: UUID статьи
        article_repository: Репозиторий статей
    
    Returns:
        Информация о статье
    """
    try:
        article_uuid = UUID(article_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid article ID format"
        )
    
    article = await article_repository.get_by_id(article_uuid)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    dto = article_to_dto(article)
    return ArticleResponse(
        id=str(dto.id),
        arxiv_id=dto.arxiv_id,
        title=dto.title,
        authors=dto.authors,
        abstract=dto.abstract,
        published_date=dto.published_date.isoformat() if dto.published_date else None,
        categories=dto.categories,
        pdf_url=dto.pdf_url,
        tex_url=dto.tex_url,
        local_pdf_path=dto.local_pdf_path,
        local_tex_path=dto.local_tex_path,
        parsed_content=dto.parsed_content
    )

