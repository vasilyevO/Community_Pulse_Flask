"""Маршруты сущности «вопрос» (см. эталон ``routers/questions``).

CRUD по контракту проекта: список отдаётся обёрткой ``items``/``count``,
детальный ответ включает статистику и вложенную категорию. При указании
``category_id`` проверяется существование категории. Ошибки — в едином
формате ``ErrorResponse``.
"""

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.models import db, Question, Category

from app.schemas.questions import QuestionCreate, QuestionUpdate
from app.schemas.statistics import StatisticsRead

from app.contracts import *


questions_bp = Blueprint('questions', __name__)


def _check_category(category_id: int | None) -> tuple | None:
    """Проверяет существование указанной категории.

    Args:
        category_id: Идентификатор категории или ``None``.

    Returns:
        Ответ 404 ``ErrorResponse``, если категория не найдена, иначе
        ``None``.
    """
    if category_id is None:
        return None
    if db.session.get(Category, category_id) is None:
        error = ErrorResponse(error=f'Category not found with id={category_id}')
        return jsonify(error.model_dump()), 404
    return None


@questions_bp.route('/', methods=['GET', 'POST'])
def questions():
    """Список вопросов (GET) или создание вопроса (POST).

    Returns:
        GET — обёртка ``items``/``count`` (200); POST — созданный вопрос
        (201) либо ответ об ошибке (400/404).
    """
    if request.method == 'GET':
        items = Question.query.all()
        result = QuestionListResponse(
            items=[QuestionResponse.model_validate(item) for item in items],
            count=len(items),
        )
        return jsonify(result.model_dump()), 200

    try:
        raw = request.get_json(silent=False)
    except Exception:
        return jsonify(ErrorResponse(error='JSON is not valid').model_dump()), 400

    if not raw:
        return jsonify(ErrorResponse(error='No data').model_dump()), 400

    try:
        data = QuestionCreate.model_validate(raw)
    except ValidationError:
        return jsonify(ErrorResponse(error='Data is not valid').model_dump()), 400

    category_error = _check_category(data.category_id)
    if category_error is not None:
        return category_error

    question = Question(**data.model_dump())
    db.session.add(question)
    db.session.commit()
    return jsonify(QuestionResponse.model_validate(question).model_dump()), 201


@questions_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def question(id):
    """Чтение (GET), обновление (PUT) или удаление (DELETE) вопроса.

    Args:
        id: Идентификатор вопроса.

    Returns:
        GET — вопрос со статистикой (200); PUT — обновлённый вопрос (200);
        DELETE — пустое тело (204); либо ответ об ошибке (400/404).
    """
    question = db.session.get(Question, id)
    if not question:
        return jsonify(
            ErrorResponse(error=f'Question not found with id={id}').model_dump()
        ), 404

    if request.method == 'GET':
        stats = (
            StatisticsRead.model_validate(question.statistics)
            if question.statistics else None
        )
        result = QuestionDetailResponse.model_validate(question)
        result.statistics = stats
        return jsonify(result.model_dump(exclude_none=True)), 200

    if request.method == 'PUT':
        try:
            raw = request.get_json(silent=False)
        except Exception:
            return jsonify(ErrorResponse(error='JSON is not valid').model_dump()), 400

        if not raw:
            return jsonify(ErrorResponse(error='No data').model_dump()), 400

        try:
            data = QuestionUpdate.model_validate(raw)
        except ValidationError:
            return jsonify(ErrorResponse(error='Data is not valid').model_dump()), 400

        category_error = _check_category(data.category_id)
        if category_error is not None:
            return category_error

        if data.text is not None:
            question.text = data.text
        question.category_id = data.category_id
        db.session.commit()
        return jsonify(QuestionResponse.model_validate(question).model_dump()), 200

    db.session.delete(question)
    db.session.commit()
    return '', 204
