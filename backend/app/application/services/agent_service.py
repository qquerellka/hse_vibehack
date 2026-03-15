"""
Сервис для работы с агентами анализа статей.

ВАЖНО: Этот модуль содержит МОКИ (заглушки) для агентов.
Реальная реализация агентов (DescribeAgent, EvalAgent, WriterAgent)
будет добавлена другим разработчиком.

Все методы помечены как МОКИ и возвращают тестовые данные.
"""

from typing import List, Optional
from uuid import UUID
from app.application.dto.evaluation_dto import EvaluationDTO
from app.application.dto.review_dto import ReviewDTO


class AgentService:
    """
    Сервис для работы с агентами анализа статей.
    
    ⚠️ МОК-РЕАЛИЗАЦИЯ ⚠️
    Этот сервис содержит заглушки для:
    - DescribeAgent (описание изображений)
    - EvalAgent (оценка статей)
    - WriterAgent (написание обзоров)
    
    Для подключения реальных агентов замените методы этого класса.
    """

    async def describe_images(self, image_paths: List[str]) -> List[str]:
        """
        Описать изображения из статьи.
        
        ⚠️ МОК-РЕАЛИЗАЦИЯ ⚠️
        Реальная реализация должна использовать vision-модель через OpenRouter
        (как в оригинальном коде: agents/describe_agent.py:18)
        
        Args:
            image_paths: Список путей к изображениям
        
        Returns:
            Список описаний изображений
        """
        # TODO: Подключить реальный DescribeAgent
        # Ожидаемая реализация:
        # - Использование vision-модели через OpenRouter API
        # - Анализ каждого изображения
        # - Возврат структурированных описаний
        
        return [
            f"[MOCK] Описание изображения {i+1}: Это тестовое описание изображения из статьи."
            for i, _ in enumerate(image_paths)
        ]

    async def evaluate_article(
        self,
        article_id: UUID,
        article_content: str,
        image_descriptions: List[str]
    ) -> EvaluationDTO:
        """
        Оценить статью по структурированной схеме.
        
        ⚠️ МОК-РЕАЛИЗАЦИЯ ⚠️
        Реальная реализация должна использовать EvalAgent с Pydantic-схемой
        (как в оригинальном коде: agents/review_agent.py:17)
        
        Args:
            article_id: ID статьи
            article_content: Содержимое статьи
            image_descriptions: Описания изображений
        
        Returns:
            Структурированная оценка статьи
        """
        # TODO: Подключить реальный EvalAgent
        # Ожидаемая реализация:
        # - Использование LLM для анализа статьи
        # - Заполнение структурированной Pydantic-схемы оценки
        # - Возврат EvaluationDTO с баллами 1-5 и обоснованием
        
        from uuid import uuid4
        from datetime import datetime
        
        return EvaluationDTO(
            id=uuid4(),
            article_id=article_id,
            category="[MOCK] Computer Science",
            relevance="[MOCK] Статья релевантна для исследования",
            novelty_score=3,
            methodology_score=4,
            impact_score=3,
            overall_score=3,
            pros=[
                "[MOCK] Хорошая методология",
                "[MOCK] Интересные результаты"
            ],
            cons=[
                "[MOCK] Недостаточно экспериментов",
                "[MOCK] Требуется больше данных"
            ],
            justification="[MOCK] Это тестовая оценка. Реальная оценка будет генерироваться EvalAgent.",
            created_at=datetime.utcnow(),
            updated_at=None
        )

    async def write_review(
        self,
        article_id: UUID,
        article_content: str,
        image_descriptions: List[str]
    ) -> ReviewDTO:
        """
        Написать обзор статьи на русском языке.
        
        ⚠️ МОК-РЕАЛИЗАЦИЯ ⚠️
        Реальная реализация должна использовать WriterAgent
        (как в оригинальном коде: agents/writer_agent.py:19)
        Может использовать Tavily для дополнительного поиска информации.
        
        Args:
            article_id: ID статьи
            article_content: Содержимое статьи
            image_descriptions: Описания изображений
        
        Returns:
            Обзор статьи на русском языке
        """
        # TODO: Подключить реальный WriterAgent
        # Ожидаемая реализация:
        # - Использование LLM для генерации обзора на русском
        # - Возможность использования Tavily для дополнительного поиска
        # - Генерация полного обзора в Markdown формате
        # - Структура: резюме, методы, результаты, критика, применение, вердикт
        
        from uuid import uuid4
        from datetime import datetime
        
        full_text = f"""# Обзор статьи

## Резюме
[MOCK] Это тестовый обзор статьи. Реальная реализация будет генерироваться WriterAgent.

## Методы
[MOCK] Описание методов из статьи.

## Результаты
[MOCK] Основные результаты исследования.

## Критика
[MOCK] Критический анализ работы.

## Применение
[MOCK] Возможные области применения.

## Вердикт
[MOCK] Итоговое заключение по статье.
"""
        
        return ReviewDTO(
            id=uuid4(),
            article_id=article_id,
            summary="[MOCK] Краткое резюме статьи",
            methods="[MOCK] Описание методов",
            results="[MOCK] Основные результаты",
            criticism="[MOCK] Критический анализ",
            application="[MOCK] Области применения",
            verdict="[MOCK] Итоговое заключение",
            full_text=full_text,
            created_at=datetime.utcnow(),
            updated_at=None
        )

