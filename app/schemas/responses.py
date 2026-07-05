"""Pydantic-схемы сущности «ответ» (голос по вопросу).

Слой валидации: входные данные проверяются до работы с БД, выходные —
сериализуются из ORM-объектов (``from_attributes=True``). Схемы построены
по паттерну ``Base → Create/Update/Read`` (см. эталон ``schemas``).
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ResponseBase(BaseModel):
    """Базовые поля ответа.

    Attributes:
        question_id: Идентификатор вопроса, по которому подан голос.
        is_agree: ``True`` — «согласен», ``False`` — «не согласен».
    """

    question_id: Annotated[int, Field(gt=0)]
    is_agree: bool


class ResponseCreate(ResponseBase):
    """Схема входных данных при создании ответа."""


class ResponseUpdate(ResponseBase):
    """Схема входных данных при обновлении ответа.

    Attributes:
        is_agree: Значение голоса или ``None`` (частичное обновление).
    """

    is_agree: bool | None = None


class ResponseRead(ResponseBase):
    """Схема вывода ответа из ORM-объекта.

    Attributes:
        id: Идентификатор ответа.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
