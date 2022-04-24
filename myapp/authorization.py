import datetime

from flask import render_template, request
from flask_login import login_user, logout_user

from .main import app, login_manager, send_mail
from .data import db_session
from .data.db_models import User, PreRegisteredUser
from .forms import PreSignUpForm, LoginForm, PreForgotPasswordForm
from .blueprints.token import generate_confirmation_token


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return render_template('page_with_message.html', title='Logged In', message=f'Hello, {user.nickname}!')
        return render_template('login.html', title='Log In', message="Invalid login or password", form=form)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('page_with_message.html', title='Logged Out', message='Bye!')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = PreSignUpForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        aboba = db_sess.query(PreRegisteredUser).filter(PreRegisteredUser.email == form.email.data).first()
        if aboba:
            if datetime.datetime.now() - aboba.created_date < datetime.timedelta(hours=1):
                return render_template('pre_signup.html', title='Sign Up', form=form,
                                       message="You already tried to register in the last hour! Try after a while!")
            else:
                aboba.set_created_date()
        else:
            new_user = PreRegisteredUser()
            new_user.email = form.email.data
            db_sess.add(new_user)
        db_sess.commit()

        url = f'http://{request.host}/confirm_email/{generate_confirmation_token(form.email.data)}'

        confirmation_text = f'''
        <div> Hello from Aliby's blog website! This is your email confirmation link: </div>
        <div> <a href="{url}">{url}</a> </div>
        '''

        send_mail(form.email.data, 'Email confirmation', confirmation_text)
        return render_template('page_with_message.html', title='Sign Up',
                               message='An email with a link to further registration has been sent to your email!!')
    return render_template('pre_signup.html', title='Sign Up', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = PreForgotPasswordForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if ((datetime.datetime.now() - user.password_requested_date).total_seconds() < 3600
                    and user.password_requested_date != user.created_date):
                message = 'You have already tried to recover your password in the last hour, try again after a while.'
                return render_template('pre_forgot_password.html', title='Reset Password', message=message, form=form)

            user.set_password_requested_date()
            db_sess.commit()
            url = f'http://{request.host}/reset_password/{generate_confirmation_token(form.email.data)}'
            mail_text = f'''
                <div> Aliby's blog website. Password Reset Link </div>
                <div> If it's not you trying to reset your password, then just ignore this message. </div>
                <div> <a href="{url}">{url}</a> </div>
                '''
            send_mail(form.email.data, 'Password Reset Link', mail_text)
        return render_template('page_with_message.html',
                               message='An email with a link to reset password has been sent to the email!')
    return render_template('pre_forgot_password.html', title='Reset Password', form=form)
