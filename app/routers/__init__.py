"""Пакет ``routers`` — слой HTTP-маршрутов (Blueprint на сущность).

Каждый роутер подключает общий слой контрактов через
``from app.contracts import *`` и отдаёт данные/ошибки в едином формате.
"""

from app.routers.questions import questions_bp
from app.routers.categories import categories_bp
from app.routers.responses import responses_bp

__all__ = ['questions_bp', 'categories_bp', 'responses_bp']
