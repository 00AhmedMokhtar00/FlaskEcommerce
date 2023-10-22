import os
from flask import Flask
from flask_migrate import Migrate

from .models import db
from .config import projectConfig as AppConfig


def create_app(config_name='dev'):
    app = Flask(__name__)
    current_config = AppConfig[config_name]

    app.config['PROJECTS_UPLOAD_FOLDER'] = 'app/static/uploads/projects'
    upload_folder = app.config['PROJECTS_UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    app.config['SQLALCHEMY_DATABASE_URI']=current_config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_DATABASE_URI'] = current_config
    app.config.from_object(current_config)

    db.init_app(app)

    migrate = Migrate(app, db, render_as_batch=True)

    #register blueprint in the application
    from .products import product_blueprint
    app.register_blueprint(product_blueprint)
    from . import views
    app.register_blueprint(views.main_blueprint)

    return app