"""Pydantic-схемы сущности «категория».

Слой валидации: входные данные проверяются до работы с БД, выходные —
сериализуются из ORM-объектов (``from_attributes=True``). Схемы построены
по паттерну ``Base → Create/Update/Read`` (см. эталон ``schemas``).
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


CategoryName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]


class CategoryBase(BaseModel):
    """Базовые поля категории.

    Attributes:
        name: Название категории (1–100 символов, обрезаются пробелы).
    """

    name: CategoryName


class CategoryCreate(CategoryBase):
    """Схема входных данных при создании категории."""


class CategoryUpdate(CategoryBase):
    """Схема входных данных при обновлении категории.

    Attributes:
        name: Название категории или ``None`` (частичное обновление).
    """

    name: CategoryName | None = None


class CategoryRead(CategoryBase):
    """Схема вывода категории из ORM-объекта.

    Attributes:
        id: Идентификатор категории.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
