from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String

from app.models import db


class Question(db.Model):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id')
    )

    category: Mapped['Category'] = relationship(back_populates='questions')
    statistics: Mapped['Statistics'] = relationship(
        back_populates='question',
        uselist=False,
        cascade='all, delete-orphan',
    )
    responses: Mapped[list['Response']] = relationship(
        back_populates='question',
        cascade='all, delete-orphan',
    )

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'id={self.id}, text={self.text}'
