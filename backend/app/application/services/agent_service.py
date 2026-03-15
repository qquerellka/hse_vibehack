"""Сервис для работы с агентами анализа статей."""
import re
import asyncio
from typing import List
from uuid import UUID, uuid4
from datetime import datetime

from app.application.dto.evaluation_dto import EvaluationDTO
from app.application.dto.review_dto import ReviewDTO
from app.infrastructure.config.settings import settings


class AgentService:
    """
    Сервис для работы с агентами анализа статей.

    Использует DescribeAgent, EvalAgent и WriterAgent из LangGraph
    для описания изображений, оценки статей и написания обзоров.
    """

    def __init__(self):
        self._describe_agent = None
        self._eval_agent = None
        self._writer_agent = None

    def _get_describe_agent(self):
        if self._describe_agent is None:
            from app.infrastructure.agents.describe_agent import DescribeAgent

            self._describe_agent = DescribeAgent(
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
            )
        return self._describe_agent

    def _get_eval_agent(self):
        if self._eval_agent is None:
            from app.infrastructure.agents.eval_agent import EvalAgent

            self._eval_agent = EvalAgent(
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
            )
        return self._eval_agent

    def _get_writer_agent(self):
        if self._writer_agent is None:
            from app.infrastructure.agents.writer_agent import WriterAgent

            self._writer_agent = WriterAgent(
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
                tavily_api_key=settings.TAVILY_API_KEY,
            )
        return self._writer_agent

    async def describe_images(self, image_paths: List[str]) -> List[str]:
        """Описать изображения из статьи с помощью vision-модели."""
        agent = self._get_describe_agent()
        descriptions = []
        for path in image_paths:
            try:
                desc = await asyncio.to_thread(agent.run, path)
                descriptions.append(desc)
            except Exception as e:
                descriptions.append(f"Не удалось описать изображение: {e}")
        return descriptions

    async def evaluate_article(
        self,
        article_id: UUID,
        article_content: str,
        image_descriptions: List[str],
    ) -> EvaluationDTO:
        """Оценить статью с помощью EvalAgent."""
        agent = self._get_eval_agent()

        # Build combined content (same format as GraphMAS)
        if image_descriptions:
            combined = (
                f"=== ОПИСАНИЯ ИЗОБРАЖЕНИЙ ({len(image_descriptions)} шт.) ===\n"
                + "\n\n".join(image_descriptions)
                + f"\n\n=== ТЕКСТ СТАТЬИ ===\n{article_content}"
            )
        else:
            combined = article_content

        result = await asyncio.to_thread(
            agent.run_with_state, {"messages": combined, "review": None}
        )

        review_obj = result.get("review")
        if review_obj is None:
            # Fallback with default scores if agent fails
            return EvaluationDTO(
                id=uuid4(),
                article_id=article_id,
                category="Unknown",
                relevance="Не удалось оценить",
                novelty_score=3,
                methodology_score=3,
                impact_score=3,
                overall_score=3,
                pros=["Не удалось выполнить оценку"],
                cons=["Агент не вернул результат"],
                justification="EvalAgent не смог обработать статью. Попробуйте позже.",
                created_at=datetime.utcnow(),
                updated_at=None,
            )

        return EvaluationDTO(
            id=uuid4(),
            article_id=article_id,
            category=review_obj.nlp_category,
            relevance="Relevant" if review_obj.is_relevant else "Not relevant",
            novelty_score=review_obj.scores.novelty,
            methodology_score=review_obj.scores.rigor,
            impact_score=review_obj.scores.impact,
            overall_score=review_obj.scores.overall,
            pros=review_obj.pros,
            cons=review_obj.cons,
            justification=review_obj.reasoning,
            created_at=datetime.utcnow(),
            updated_at=None,
        )

    async def write_review(
        self,
        article_id: UUID,
        article_content: str,
        image_descriptions: List[str],
    ) -> ReviewDTO:
        """Написать обзор статьи с помощью WriterAgent."""
        agent = self._get_writer_agent()

        if image_descriptions:
            combined = (
                f"=== ОПИСАНИЯ ИЗОБРАЖЕНИЙ ({len(image_descriptions)} шт.) ===\n"
                + "\n\n".join(image_descriptions)
                + f"\n\n=== ТЕКСТ СТАТЬИ ===\n{article_content}"
            )
        else:
            combined = article_content

        full_text = await asyncio.to_thread(agent.run, combined)

        sections = self._parse_review_sections(full_text)

        return ReviewDTO(
            id=uuid4(),
            article_id=article_id,
            summary=sections.get("summary", ""),
            methods=sections.get("methods", ""),
            results=sections.get("results", ""),
            criticism=sections.get("criticism", ""),
            application=sections.get("application", ""),
            verdict=sections.get("verdict", ""),
            full_text=full_text,
            created_at=datetime.utcnow(),
            updated_at=None,
        )

    @staticmethod
    def _parse_review_sections(markdown_text: str) -> dict:
        """Parse WriterAgent markdown output into ReviewDTO sections.

        The writer produces sections with Russian headers like:
        - Краткое резюме / Executive Summary -> summary
        - Ключевые идеи и методы -> methods
        - Результаты и эксперименты -> results
        - Сильные и слабые стороны / Critique -> criticism
        - Практическое применение -> application
        - Вердикт -> verdict
        """
        section_keywords = {
            "summary": ["резюме", "executive summary", "summary"],
            "methods": ["ключевые идеи", "метод", "methods", "идеи и методы"],
            "results": ["результат", "эксперимент", "results"],
            "criticism": [
                "сильные и слабые",
                "critique",
                "критик",
                "слабые стороны",
            ],
            "application": ["применение", "практическое", "application"],
            "verdict": ["вердикт", "verdict", "заключение"],
        }

        sections = {
            "summary": "",
            "methods": "",
            "results": "",
            "criticism": "",
            "application": "",
            "verdict": "",
        }

        # Split by markdown headers (## or **...**)
        parts = re.split(r"\n(?=#{1,3}\s|(?:\*\*[^*]+\*\*))", markdown_text)

        current_key = "summary"  # default first section
        for part in parts:
            header_match = re.match(r"^#{1,3}\s*(.+)", part) or re.match(
                r"^\*\*(.+?)\*\*", part
            )
            if header_match:
                header_text = header_match.group(1).lower().strip()
                for key, keywords in section_keywords.items():
                    if any(kw in header_text for kw in keywords):
                        current_key = key
                        break
            sections[current_key] += part.strip() + "\n\n"

        return {k: v.strip() for k, v in sections.items()}
