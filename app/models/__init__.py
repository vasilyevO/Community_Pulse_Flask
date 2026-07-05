from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from .category import Category
from .questions import Question
from .responses import Response
from .statistics import Statistics

__all__ = ['db', 'migrate', 'Category', 'Question', 'Response', 'Statistics']
