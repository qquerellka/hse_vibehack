from typing import Annotated, TypedDict
from uuid import uuid4
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver


class WriterState(TypedDict):
    messages: Annotated[list, add_messages]


class WriterAgent:
    def __init__(
        self,
        api_key: str = "",
        base_url: str = "https://openrouter.ai/api/v1",
        tavily_api_key: str = "",
    ):
        self._api_key = api_key
        self._base_url = base_url
        self.tools = [TavilySearchResults(api_key=tavily_api_key)]
        self.model = ChatOpenAI(
            model="arcee-ai/trinity-large-preview:free",
            api_key=api_key,
            base_url=base_url,
            max_retries=2,
            max_tokens=9128,
            temperature=0.7,
        ).bind_tools(self.tools)

        self.tool_node = ToolNode(self.tools)
        self.memory = MemorySaver()
        self.graph = self._build_graph(WriterState)

    def _build_graph(self, state: WriterState):
        graph = StateGraph(state)
        graph.add_node("write_review", self._write_review)
        graph.add_node("tools", self.tool_node)
        graph.add_edge(START, "write_review")
        graph.add_conditional_edges(
            "write_review",
            self._should_continue,
            {
                "tools": "tools",
                "end": END
            }
        )
        graph.add_edge("tools", "write_review")
        return graph.compile(checkpointer=self.memory)

    def _write_review(self, state: WriterState) -> WriterState:
        system_prompt = SystemMessage(
            content="""Ты — экспертный технический писатель и аналитик в области ИИ.
Твоя задача — создать глубокий, структурированный и увлекательный обзор научной статьи для профессионального сообщества (ученых, инженеров ML).

### ВАЖНО:
Входные данные содержат:
1. **Описания изображений** (графики, схемы, таблицы) — помечены как "=== ОПИСАНИЯ ИЗОБРАЖЕНИЙ ===" (в начале)
2. **Текст статьи** (из LaTeX .tex файлов или PDF) — помечен как "=== ТЕКСТ СТАТЬИ ==="

Используй описания изображений в обзоре:
- Ссылайся на графики и таблицы при описании результатов.
- Объясняй схемы архитектуры, если они есть.
- Упоминай визуальные доказательства преимуществ метода.

### ТВОЯ МИССИЯ:
- Превратить сложный научный текст в понятный, но не упрощенный обзор.
- Выделить самое главное ("соль"), отбросив воду.
- Дать критическую оценку, а не просто пересказать аннотацию.

### СТРУКТУРА ОБЗОРА (ОБЯЗАТЕЛЬНО):

1. **Краткое резюме (Executive Summary):**
   - О чем статья в одном абзаце? Какую проблему решает? Какой главный вклад (contribution)?

2. **Ключевые идеи и методы:**
   - Как именно работает предложенный метод? (Используй термины, но объясняй их суть).
   - В чем отличие от SOTA (предыдущих лучших решений)?

3. **Результаты и эксперименты:**
   - На каких бенчмарках тестировали?
   - Какие метрики улучшились и на сколько? (Цифры важны!).

4. **Сильные и слабые стороны (Critique):**
   - Плюсы: Что авторы сделали круто?
   - Минусы: Чего не хватает? Где метод может сломаться? Были ли честные абляции?

5. **Практическое применение:**
   - Кому и зачем это нужно прямо сейчас? Где это можно внедрить?

6. **Вердикт:**
   - Стоит ли читать фулл? (Мастхэв / Проходная / Интересно только узким спецам).

### СТИЛЬ:
- Язык: **Русский** (профессиональный, живой).
- Формат: Markdown (жирные заголовки, списки, выделение ключевых мыслей).
- Тон: Экспертный, объективный, слегка критичный.
- Объем: Достаточный для понимания сути без чтения оригинала (около 500-800 слов).

Используй поиск (Tavily), если встречаешь неизвестные термины или хочешь найти контекст (кто авторы, где опубликовано)."""
        )

        last_message = state['messages'][-1]
        article_text = last_message.content if hasattr(last_message, 'content') else str(last_message)

        user_prompt = HumanMessage(
            content=f"""Напиши обзор на основе следующего текста статьи:\n\n{article_text}"""
        )

        response = self.model.invoke([system_prompt, user_prompt])

        return {
            "messages": [response]
        }

    def _generate_quiz(self, state: WriterState) -> WriterState:
        system_prompt = SystemMessage(
            content="""Ты — эксперт по созданию образовательных тестов на основе научных статей.

### ЗАДАЧА:
Создай короткий тест (5 вопросов) по содержанию статьи для закрепления материала. Тест должен проверять понимание ключевых идей, а не запоминание мелких деталей.

### ФОРМАТ КАЖДОГО ВОПРОСА:
```
**Вопрос N.** <текст вопроса>

A) <вариант>
B) <вариант>
C) <вариант>
D) <вариант>

Правильный ответ: <буква>) <пояснение в 1-2 предложения, почему этот ответ верный>
```

### ТРЕБОВАНИЯ К ВОПРОСАМ:
1. **Вопрос 1** — о главной проблеме/задаче, которую решает статья.
2. **Вопрос 2** — о предложенном методе/архитектуре.
3. **Вопрос 3** — о ключевых результатах/метриках.
4. **Вопрос 4** — о сравнении с предыдущими подходами (SOTA).
5. **Вопрос 5** — о практическом применении или ограничениях метода.

### СТИЛЬ:
- Язык: **Русский**.
- Варианты ответов должны быть правдоподобными (не очевидно неправильными).
- Пояснения к ответам — краткие, но информативные.
- Формат: Markdown."""
        )

        last_message = state['messages'][-1]
        article_text = last_message.content if hasattr(last_message, 'content') else str(last_message)

        user_prompt = HumanMessage(
            content=f"""Создай тест из 5 вопросов по следующей статье:\n\n{article_text}"""
        )

        model_no_tools = ChatOpenAI(
            model="arcee-ai/trinity-large-preview:free",
            api_key=self._api_key,
            base_url=self._base_url,
            max_retries=2,
            max_tokens=9128,
            temperature=0.5,
        )

        response = model_no_tools.invoke([system_prompt, user_prompt])

        return {
            "messages": [response]
        }

    def run_quiz(self, paper_text: str) -> str:
        state = {"messages": [HumanMessage(content=paper_text)]}
        result = self._generate_quiz(state)
        return result["messages"][-1].content

    def _should_continue(self, state: WriterState) -> str:
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return "end"

    def run(self, paper: str):
        # Generate unique thread_id per invocation to avoid conflicts
        thread_id = f"writer-agent-{uuid4().hex[:8]}"
        initial_state = {
            "messages": [HumanMessage(content=paper)]
        }
        response = self.graph.invoke(
            initial_state,
            config={"configurable": {"thread_id": thread_id}}
        )
        return response["messages"][-1].content

    def run_with_state(self, write_state: dict):
        thread_id = f"writer-agent-{uuid4().hex[:8]}"
        return self.graph.invoke(
            write_state,
            config={"configurable": {"thread_id": thread_id}}
        )
