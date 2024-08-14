from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.admin import admin
from app import db
from app.auth.models import User, Role
from .forms import RoleForm, UserForm

@admin.route("/")
@login_required
def dashboard():
    if current_user.role.name != 'Admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.dashboard'))
    return render_template('admin/dashboard.html', title='Admin Dashboard')

@admin.route('/manage_roles', methods=['GET', 'POST'])
def manage_roles():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data)
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully', 'success')
        return redirect(url_for('admin.manage_roles'))
    
    roles = Role.query.all()
    return render_template('admin/manage_roles.html', roles=roles, form=form)

@admin.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    form = UserForm()
    if form.validate_on_submit():
        role_id = form.role.data
        role = Role.query.get(role_id) if role_id != 0 else None
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.role = role
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('admin.manage_users'))
    
    form.role.choices = [(0, 'Select a Role')] + [(role.id, role.name) for role in Role.query.all()]
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/manage_users.html', users=users, roles=roles, form=form)

@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if request.method == 'GET':
        form.role.choices = [(0, 'Select a Role')] + [(role.id, role.name) for role in Role.query.all()]
        form.role.data = user.role_id if user.role else 0
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        user.role = Role.query.get(form.role.data) if form.role.data != 0 else None
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin.manage_users'))

