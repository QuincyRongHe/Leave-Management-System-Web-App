from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flask import session
# import connect
# import mysql.connector
from ..auth.model import check_password, get_username_by_user_id




class ChangePWDForm(FlaskForm):

    old_password = PasswordField('Old password', validators=[DataRequired(), Length(min=8, max=20)])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=20)])
    re_new_password = PasswordField('Repeat new password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Confirm new password!')

    def validate_old_password(form, field):
        input_pwd = field.data
        print(input_pwd)
        username = get_username_by_user_id(session['userID'])
        if not check_password(username, input_pwd):
            raise ValidationError('Incorrect old password!')
        
    def validate_re_new_password(form, field):
        if field.data != form.new_password.data:
            raise ValidationError('Passwords do not match!')


class SearchEmployeeForm(FlaskForm):

    search = StringField('Search', validators=[Length(max=20)], render_kw={"placeholder": "Search by name"})
    select_role = SelectField('Role', validators=[DataRequired()], coerce=int, choices=[(-1, ''), (1, 'Employee'), (2, 'Approval Manager'), (3, 'Admin')])
    submit = SubmitField('Search')
    reset = SubmitField('Reset')
