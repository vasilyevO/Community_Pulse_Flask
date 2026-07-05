from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.models import db


class Statistics(db.Model):
    __tablename__ = 'statistics'

    question_id: Mapped[int] = mapped_column(
        ForeignKey('questions.id'), primary_key=True
    )
    agree_count: Mapped[int] = mapped_column(nullable=False, default=0)
    disagree_count: Mapped[int] = mapped_column(nullable=False, default=0)

    question: Mapped['Question'] = relationship(back_populates='statistics')

    def __str__(self):
        return (f'question_id={self.question_id}, agree_count={self.agree_count}, '
                f'disagree_count={self.disagree_count}')

    def __repr__(self):
        return (f'question_id={self.question_id}, agree_count={self.agree_count}, '
                f'disagree_count={self.disagree_count}')
