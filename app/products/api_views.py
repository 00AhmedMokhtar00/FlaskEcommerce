from flask import jsonify, request, Blueprint

from .models import Product

products_api_blueprint = Blueprint('api', __name__, url_prefix='/api')



@products_api_blueprint.route('/products', methods=['GET'])
def api_list_products():
    products = Product.get_all_objects()
    return jsonify([product.to_dict() for product in products])

@products_api_blueprint.route('/products/<int:id>', methods=['GET'])
def api_get_product(id):
    product = Product.get_specific_product(id)
    return jsonify(product.to_dict())

@products_api_blueprint.route('/products', methods=['POST'])
def api_create_product():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid JSON data'}), 400

    product = Product.create_product(data)
    return jsonify(product.to_dict()), 201

@products_api_blueprint.route('/products/<int:id>', methods=['PUT', 'PATCH'])
def api_update_product(id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid JSON data'}), 400

    product = Product.edit_product(id, data)

    if not product:
        return jsonify({'message': 'Product not found or not updated'}), 404

    return jsonify(product.to_dict())


@products_api_blueprint.route('/products/<int:id>', methods=['DELETE'])
def api_delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    Product.delete_product(id)
    return jsonify({'message': 'Product deleted successfully'}), 204
