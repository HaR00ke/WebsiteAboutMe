from flask import render_template, request
from flask_login import login_user, logout_user

from .main import app, login_manager, send_mail
from .data import db_session
from .data.db_models.user import User
from .forms import PreSignUpForm, LoginForm 
from .blueprints.confirm_mail_api.token import generate_confirmation_token


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
            return render_template('page_with_message.html', message=f'Hello, {user.nickname}!')
        return render_template('login.html',
                               message="Invalid login or password",
                               form=form)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('page_with_message.html', message=f'Bye!')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = PreSignUpForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('pre_signup.html', title='Sign Up', form=form,
                                   message="User with this email already exists!")

        confirmation_text = '''
        <div> Hello from Aliby's blog website! This is your email confirmation link: </div>
        <a href="{url}">{url}</a>
        '''

        url = f'http://{request.host}/confirm_email/{generate_confirmation_token(form.email.data)}'
        send_mail(form.email.data, 'Email confirmation', confirmation_text.format(url=url))

        msg = 'An email with a link to further registration has been sent to your email!!'
        return render_template('page_with_message.html', message=msg)
    return render_template('pre_signup.html', title='Sign Up', form=form)
