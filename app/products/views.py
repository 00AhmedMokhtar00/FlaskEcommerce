import os

from flask import current_app, request,render_template, redirect, url_for
app = current_app
from werkzeug.utils import secure_filename

from app.categories.models import Category
from .models import Product
from . import product_blueprint

# List products
@product_blueprint.route('', endpoint='products_index')
def index():
    products = Product.get_all_objects()
    return render_template('products/index.html', products=products)

@product_blueprint.route('<int:id>', endpoint='show')
def show(id):
    product = Product.get_specific_product(id)
    return  render_template('products/product_detail.html', product=product)

# Add product
@product_blueprint.route('/create', endpoint='create', methods=['GET', 'POST'] )
def create():
    if request.method == 'POST':
        image = request.files['image']

        filename=''
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['PROJECTS_UPLOAD_FOLDER'], filename)
            image.save(image_path)

        product = Product.create_product(request.form, filename)


        return redirect(url_for('products.products_index'))
    categories = Category.get_all_objects()
    return render_template('products/add_product.html', categories=categories)

# Update product
@product_blueprint.route('/update/<int:id>', endpoint='update', methods=['GET', 'POST'])
def update(id):
    product = Product.get_specific_product(id)

    if request.method == 'POST':
        image = request.files['image']

        filename=''
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['PROJECTS_UPLOAD_FOLDER'], filename)
            image.save(image_path)

        updated_product = Product.edit_product(id, request.form, filename)
        return redirect(url_for('products.products_index'))
    categories = Category.get_all_objects()
    return render_template('products/edit_product.html', product=product, categories=categories)


# Delete product
@product_blueprint.route('/delete/<int:id>', endpoint='delete')
def delete_product(id):
    product = Product.delete_product(id)
    return redirect(url_for('products.products_index'))