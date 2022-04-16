from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class PreSignUpForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Next Step')


class SignUpForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired()], render_kw={'disabled': True})
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat Password', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class PreForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Send mail')


class ForgotPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat New Password', validators=[DataRequired()])
    submit = SubmitField('Reset password')
