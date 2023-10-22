from flask import Blueprint, render_template


main_blueprint = Blueprint('main', __name__)


@main_blueprint.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/page_not_found.html'), 404

@main_blueprint.route('/about', endpoint='about')
def about():
    return render_template('about.html')

@main_blueprint.route('/contact', endpoint='contact')
def contact():
    return render_template('contact.html')