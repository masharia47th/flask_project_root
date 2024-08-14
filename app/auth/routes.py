from flask import render_template, url_for, flash, redirect, request
from app import db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

from . import auth
@auth.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            flash('login successful','success')
            return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
        
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
