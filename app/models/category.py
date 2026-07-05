from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String

from app.models import db


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    questions: Mapped[list['Question']] = relationship(back_populates='category')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'id={self.id}, name={self.name}'
