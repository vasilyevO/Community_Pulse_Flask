"""Pydantic-схема агрегированной статистики по вопросу.

Слой валидации/сериализации: значение ``total_count`` вычисляется на лету
как сумма голосов (``@computed_field``). Данные читаются из ORM-объекта
(``from_attributes=True``).
"""

from pydantic import BaseModel, ConfigDict, computed_field


class StatisticsRead(BaseModel):
    """Схема вывода статистики по вопросу.

    Attributes:
        question_id: Идентификатор вопроса.
        agree_count: Число голосов «согласен».
        disagree_count: Число голосов «не согласен».
    """

    model_config = ConfigDict(from_attributes=True)

    question_id: int
    agree_count: int
    disagree_count: int

    @computed_field
    @property
    def total_count(self) -> int:
        """Возвращает суммарное число голосов.

        Returns:
            Сумма ``agree_count`` и ``disagree_count``.
        """
        return self.agree_count + self.disagree_count
