"""Контракты API сущности «категория» (см. эталон).

Запросы наследуют ``Category*``-схемы слоя ``schemas``, ответы — ``*Read``;
для списка добавляется обёртка ``items``/``count``.
"""

from pydantic import BaseModel

from app.schemas import CategoryCreate, CategoryUpdate, CategoryRead


class CategoryCreateRequest(CategoryCreate):
    """Тело запроса на создание категории."""


class CategoryUpdateRequest(CategoryUpdate):
    """Тело запроса на обновление категории."""


class CategoryResponse(CategoryRead):
    """Ответ с одной категорией."""


class CategoryListResponse(BaseModel):
    """Ответ со списком категорий.

    Attributes:
        items: Список категорий.
        count: Число элементов в списке.
    """

    items: list[CategoryResponse]
    count: int
