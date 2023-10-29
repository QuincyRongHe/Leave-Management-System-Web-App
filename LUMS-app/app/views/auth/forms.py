from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                       Email()], render_kw={'class_': 'login-input-field'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'class_': 'login-input-field'})
    submit = SubmitField('Sign In', render_kw={'class_': 'login-btn'})



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')