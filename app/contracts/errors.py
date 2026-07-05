"""Единый формат ответа об ошибке API (см. эталон).

Тело ошибки описано схемами ``ErrorResponse`` и ``ErrorItem``: понятное
сообщение ``error`` и, при необходимости, список ``details`` с указанием
поля и причины.
"""

from pydantic import BaseModel


class ErrorItem(BaseModel):
    """Одна ошибка валидации конкретного поля.

    Attributes:
        field: Имя поля.
        message: Человекочитаемое описание причины.
    """

    field: str
    message: str


class ErrorResponse(BaseModel):
    """Единое тело ответа об ошибке.

    Attributes:
        error: Понятное пользователю сообщение об ошибке.
        details: Список детальных ошибок по полям (может быть пустым).
    """

    error: str
    details: list[ErrorItem] = []
