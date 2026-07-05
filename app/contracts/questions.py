"""Контракты API сущности «вопрос» (см. эталон).

Контракты собираются из схем слоя ``schemas``: запросы наследуют
``*Create``/``*Update``, ответы — ``*Read``; для списка добавляется обёртка
``items``/``count``, для детального ответа — вложенная статистика.
"""

from pydantic import BaseModel

from app.schemas import QuestionCreate, QuestionUpdate, QuestionRead
from app.schemas import StatisticsRead


class QuestionCreateRequest(QuestionCreate):
    """Тело запроса на создание вопроса."""


class QuestionUpdateRequest(QuestionUpdate):
    """Тело запроса на обновление вопроса."""


class QuestionResponse(QuestionRead):
    """Ответ с одним вопросом."""


class QuestionDetailResponse(QuestionRead):
    """Детальный ответ с вопросом и его статистикой.

    Attributes:
        statistics: Агрегированная статистика или ``None``.
    """

    statistics: StatisticsRead | None = None


class QuestionListResponse(BaseModel):
    """Ответ со списком вопросов.

    Attributes:
        items: Список вопросов.
        count: Число элементов в списке.
    """

    items: list[QuestionResponse]
    count: int
