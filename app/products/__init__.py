from flask import  Blueprint

product_blueprint= Blueprint('products', __name__, url_prefix='/products')
from . import views
