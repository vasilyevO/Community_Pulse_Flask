"""Пакет ``contracts`` — слой API-контрактов (см. эталон).

Собирает в одной точке единый формат ошибок (``ErrorItem``,
``ErrorResponse``) и контракты запросов/ответов всех сущностей. Роутеры
подключают пакет через ``from app.contracts import *``.
"""

from .errors import ErrorItem, ErrorResponse
from .questions import (
    QuestionCreateRequest,
    QuestionUpdateRequest,
    QuestionResponse,
    QuestionDetailResponse,
    QuestionListResponse,
)
from .categories import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse,
    CategoryListResponse,
)
from .responses import (
    ResponseCreateRequest,
    ResponseUpdateRequest,
    ResponseResponse,
    ResponseListResponse,
)


__all__ = [
    'ErrorItem',
    'ErrorResponse',
    'QuestionCreateRequest',
    'QuestionUpdateRequest',
    'QuestionResponse',
    'QuestionDetailResponse',
    'QuestionListResponse',
    'CategoryCreateRequest',
    'CategoryUpdateRequest',
    'CategoryResponse',
    'CategoryListResponse',
    'ResponseCreateRequest',
    'ResponseUpdateRequest',
    'ResponseResponse',
    'ResponseListResponse',
]
