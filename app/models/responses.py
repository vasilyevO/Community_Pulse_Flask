from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.models import db


class Response(db.Model):
    __tablename__ = 'responses'

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    is_agree: Mapped[bool] = mapped_column(nullable=False)

    question: Mapped['Question'] = relationship(back_populates='responses')

    def __str__(self):
        return f'id={self.id}, question_id={self.question_id}, is_agree={self.is_agree}'

    def __repr__(self):
        return f'id={self.id}, question_id={self.question_id}, is_agree={self.is_agree}'
