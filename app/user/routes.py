from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from app.user import user

@user.route("/")
@login_required
def dashboard():
    return render_template('user/dashboard.html', title='User Dashboard')
