"""Pydantic-схемы сущности «вопрос».

Слой валидации: входные данные проверяются до работы с БД, выходные —
сериализуются из ORM-объектов (``from_attributes=True``). Схемы построены
по паттерну ``Base → Create/Update/Read`` (см. эталон ``schemas``).
"""

from typing import Annotated

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
)

from app.schemas.category import CategoryRead


QuestionText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=5, max_length=100),
]


class QuestionBase(BaseModel):
    """Базовые поля вопроса.

    Attributes:
        text: Текст вопроса (5–100 символов, обрезаются пробелы).
        category_id: Идентификатор категории или ``None``. Принимается
            также под устаревшим именем ``category``.
    """

    model_config = ConfigDict(populate_by_name=True)

    text: QuestionText
    category_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices('category_id', 'category'),
    )


class QuestionCreate(QuestionBase):
    """Схема входных данных при создании вопроса."""


class QuestionUpdate(QuestionBase):
    """Схема входных данных при обновлении вопроса.

    Attributes:
        text: Текст вопроса или ``None`` (частичное обновление).
    """

    text: QuestionText | None = None


class QuestionRead(QuestionBase):
    """Схема вывода вопроса с вложенной категорией.

    Attributes:
        id: Идентификатор вопроса.
        category: Вложенная категория или ``None``.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    category: CategoryRead | None = None
