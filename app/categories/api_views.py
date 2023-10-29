from flask import Blueprint, jsonify, request

from .models import Category

categories_api_blueprint = Blueprint('categories_api', __name__, url_prefix='/api')

@categories_api_blueprint.route('/categories', methods=['GET'])
def api_list_categories():
    categories = Category.get_all_objects()
    return jsonify([category.to_dict() for category in categories])

@categories_api_blueprint.route('/categories/<int:id>', methods=['GET'])
def api_get_category(id):
    category = Category.get_specific_category(id)
    return jsonify({'id': category.id, 'name': category.name})

@categories_api_blueprint.route('/categories', methods=['POST'])
def api_create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    category = Category.create_category(data)
    return jsonify({'id': category.id, 'name': category.name}), 201


@categories_api_blueprint.route('/categories/<int:id>', methods=['PUT', 'PATCH'])
def api_update_category(id):
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    Category.edit_category(id, data)
    category = Category.get_specific_category(id)
    return jsonify({'id': category.id, 'name': category.name})


@categories_api_blueprint.route('/categories/<int:id>', methods=['DELETE'])
def api_delete_category(id):
    Category.delete_category(id)
    return jsonify({'message': 'Category deleted successfully'}), 204
