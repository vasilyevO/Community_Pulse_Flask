"""Маршруты сущности «категория» (см. эталон ``routers/questions``).

CRUD по контракту проекта: список отдаётся обёрткой ``items``/``count``.
Ошибки — в едином формате ``ErrorResponse``.
"""

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.models import db, Category

from app.schemas.category import CategoryCreate, CategoryUpdate

from app.contracts import *


categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/', methods=['GET', 'POST'])
def categories():
    """Список категорий (GET) или создание категории (POST).

    Returns:
        GET — обёртка ``items``/``count`` (200); POST — созданная категория
        (201) либо ответ об ошибке (400).
    """
    if request.method == 'GET':
        items = Category.query.all()
        result = CategoryListResponse(
            items=[CategoryResponse.model_validate(item) for item in items],
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
        data = CategoryCreate.model_validate(raw)
    except ValidationError:
        return jsonify(ErrorResponse(error='Data is not valid').model_dump()), 400

    category = Category(**data.model_dump())
    db.session.add(category)
    db.session.commit()
    return jsonify(CategoryResponse.model_validate(category).model_dump()), 201


@categories_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def category(id):
    """Чтение (GET), обновление (PUT) или удаление (DELETE) категории.

    Args:
        id: Идентификатор категории.

    Returns:
        GET — категория (200); PUT — обновлённая категория (200);
        DELETE — пустое тело (204); либо ответ об ошибке (400/404).
    """
    category = db.session.get(Category, id)
    if not category:
        return jsonify(
            ErrorResponse(error=f'Category not found with id={id}').model_dump()
        ), 404

    if request.method == 'GET':
        return jsonify(CategoryResponse.model_validate(category).model_dump()), 200

    if request.method == 'PUT':
        try:
            raw = request.get_json(silent=False)
        except Exception:
            return jsonify(ErrorResponse(error='JSON is not valid').model_dump()), 400

        if not raw:
            return jsonify(ErrorResponse(error='No data').model_dump()), 400

        try:
            data = CategoryUpdate.model_validate(raw)
        except ValidationError:
            return jsonify(ErrorResponse(error='Data is not valid').model_dump()), 400

        if data.name is not None:
            category.name = data.name
        db.session.commit()
        return jsonify(CategoryResponse.model_validate(category).model_dump()), 200

    db.session.delete(category)
    db.session.commit()
    return '', 204
