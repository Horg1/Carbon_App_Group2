from flask import Blueprint, render_template

methodology = Blueprint('methodology', __name__)


@methodology.route('/methodology')
def methodology_home():
    return render_template('methodology.html', title='methodology')
