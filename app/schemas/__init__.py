"""Пакет ``schemas`` — слой валидации (Pydantic).

Реэкспортирует схемы всех сущностей, чтобы слой контрактов подключал их
одной строкой ``from app.schemas import *`` (см. эталон).
"""

from .statistics import StatisticsRead
from .category import CategoryBase, CategoryCreate, CategoryUpdate, CategoryRead
from .responses import ResponseBase, ResponseCreate, ResponseUpdate, ResponseRead
from .questions import QuestionBase, QuestionCreate, QuestionUpdate, QuestionRead


__all__ = [
    'StatisticsRead',
    'CategoryBase',
    'CategoryCreate',
    'CategoryUpdate',
    'CategoryRead',
    'ResponseBase',
    'ResponseCreate',
    'ResponseUpdate',
    'ResponseRead',
    'QuestionBase',
    'QuestionCreate',
    'QuestionUpdate',
    'QuestionRead',
]
