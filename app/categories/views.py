from flask import request,render_template, redirect, url_for

from .models import Category
from . import category_blueprint


@category_blueprint.route('', endpoint='categories_index')
def category_index():
    categories = Category.get_all_objects()
    return render_template('categories/category_index.html', categories=categories)

@category_blueprint.route('<int:id>', endpoint='show')
def show(id):
    category = Category.get_specific_category(id)
    return  render_template('categories/show.html', category=category)


@category_blueprint.route('/create', endpoint='create_category',methods = ['GET', 'POST'])
def create():
    if request.method=='POST':
        category = Category.create_category(request.form)
        return redirect(url_for('categories.categories_index'))

    return render_template('categories/create.html')


@category_blueprint.route('/delete/<int:id>', endpoint='delete')
def delete_category(id):
    category = Category.delete_category(id)
    return redirect(url_for('categories.categories_index'))