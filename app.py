from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

""" Connect to database ====> sqlite """
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)


# List products
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/page_not_found.html')

# Product details
@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

# Add product
@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files['image']

        filename = ""
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

        new_product = Product(title=title, description=description, price=price, image=filename)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

# Edit product
@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get(id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        new_image = request.files.get('image')  # Get the uploaded image

        if new_image:
            # Save the new image if provided
            filename = secure_filename(new_image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            new_image.save(image_path)
            product.image = filename  # Update the product's image

        product.title = title
        product.description = description
        product.price = price
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)

# Delete product
@app.route('/product/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
