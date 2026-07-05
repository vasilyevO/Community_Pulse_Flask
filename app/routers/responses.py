"""Маршруты сущности «ответ» (голос по вопросу; см. эталон).

CRUD по контракту проекта: список отдаётся обёрткой ``items``/``count``.
При создании проверяется существование вопроса. Ошибки — в едином формате
``ErrorResponse``.
"""

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.models import db, Question
from app.models.responses import Response as ResponseModel

from app.schemas.responses import ResponseCreate, ResponseUpdate

from app.contracts import *


responses_bp = Blueprint('responses', __name__)


@responses_bp.route('/', methods=['GET', 'POST'])
def responses():
    """Список ответов (GET) или создание ответа (POST).

    Returns:
        GET — обёртка ``items``/``count`` (200); POST — созданный ответ
        (201) либо ответ об ошибке (400/404).
    """
    if request.method == 'GET':
        items = ResponseModel.query.all()
        result = ResponseListResponse(
            items=[ResponseResponse.model_validate(item) for item in items],
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
        data = ResponseCreate.model_validate(raw)
    except ValidationError:
        return jsonify(ErrorResponse(error='Data is not valid').model_dump()), 400

    if db.session.get(Question, data.question_id) is None:
        return jsonify(
            ErrorResponse(
                error=f'Question not found with id={data.question_id}'
            ).model_dump()
        ), 404

    response = ResponseModel(**data.model_dump())
    db.session.add(response)
    db.session.commit()
    return jsonify(ResponseResponse.model_validate(response).model_dump()), 201


@responses_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def response(id):
    """Чтение (GET), обновление (PUT) или удаление (DELETE) ответа.

    Args:
        id: Идентификатор ответа.

    Returns:
        GET — ответ (200); PUT — обновлённый ответ (200); DELETE —
        пустое тело (204); либо ответ об ошибке (400/404).
    """
    response = db.session.get(ResponseModel, id)
    if not response:
        return jsonify(
            ErrorResponse(error=f'Response not found with id={id}').model_dump()
        ), 404

    if request.method == 'GET':
        return jsonify(ResponseResponse.model_validate(response).model_dump()), 200

    if request.method == 'PUT':
        try:
            raw = request.get_json(silent=False)
        except Exception:
            return jsonify(ErrorResponse(error='JSON is not valid').model_dump()), 400

        if not raw:
            return jsonify(ErrorResponse(error='No data').model_dump()), 400

        try:
            data = ResponseUpdate.model_validate(raw)
        except ValidationError:
            return jsonify(ErrorResponse(error='Data is not valid').model_dump()), 400

        if data.is_agree is not None:
            response.is_agree = data.is_agree
        db.session.commit()
        return jsonify(ResponseResponse.model_validate(response).model_dump()), 200

    db.session.delete(response)
    db.session.commit()
    return '', 204
