from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/home')
def home_home():
    return render_template('home.html')

@home.route("/about")
def about():
    return render_template("about.html", title = "About Us")