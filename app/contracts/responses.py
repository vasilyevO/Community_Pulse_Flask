"""Контракты API сущности «ответ» (голос по вопросу; см. эталон).

Запросы наследуют ``Response*``-схемы слоя ``schemas``, ответы — ``*Read``;
для списка добавляется обёртка ``items``/``count``.
"""

from pydantic import BaseModel

from app.schemas import ResponseCreate, ResponseUpdate, ResponseRead


class ResponseCreateRequest(ResponseCreate):
    """Тело запроса на создание ответа."""


class ResponseUpdateRequest(ResponseUpdate):
    """Тело запроса на обновление ответа."""


class ResponseResponse(ResponseRead):
    """Ответ с одним голосом."""


class ResponseListResponse(BaseModel):
    """Ответ со списком голосов.

    Attributes:
        items: Список ответов.
        count: Число элементов в списке.
    """

    items: list[ResponseResponse]
    count: int
