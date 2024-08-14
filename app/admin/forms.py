from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from app.auth.models import Role

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Add Role')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add User')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        roles = [(role.id, role.name) for role in Role.query.all()]
        self.role.choices = [(0, 'Select a Role')] + roles  # 0 or any non-existent ID for placeholder
