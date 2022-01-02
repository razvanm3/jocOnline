from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
      email = StringField('Email Address', validators=[DataRequired()])
      password = PasswordField('Password', validators=[DataRequired()])
      confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
      #birth_date = DateField('Birth Date', validators=[DataRequired()])
      submit = SubmitField ("Sign Up")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')