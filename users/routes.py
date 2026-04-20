from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from capp import bcrypt, db
from capp.models import User
from capp.users.forms import LoginForm, RegistrationForm


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=user_hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Now, you are able to login!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful. You can start to use the app.', 'success')
            return redirect(url_for('home.home_home'))

        flash('Login failed. Please check your credentials and try again.', 'danger')
        return redirect(url_for('users.login'))

    return render_template('users/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home.home_home'))


