from flask import Blueprint, render_template

from myapp.data.db_session import create_session
from myapp.data.db_models import User
from myapp.forms import SignUpForm
from ..token import confirm_token

blueprint = Blueprint(
    'email_confirmation',
    __name__,
    template_folder='templates'
)


@blueprint.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return render_template('page_with_message.html', message="The email confirmation link doesn't exist or expired!"
                                                                 "\nSign Up again!")
    form = SignUpForm()
    form.email.data = email

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup.html', title='Sign Up',
                                   form=form, message="Passwords don't match!")
        if len(form.password.data) < 8:
            return render_template('signup.html', title='Sign Up',
                                   form=form, message="Password is too short!")

        if not 4 <= len(form.nickname.data) <= 20:
            return render_template('signup.html', title='Sign Up',
                                   form=form, message="The length of the nickname must be between 4 and 20!")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('signup.html', title='Sign Up',
                                   form=form, message="User with this email already exists!", )
        user = User()
        user.nickname = form.nickname.data
        user.email = email
        user.confirmed = False
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return render_template('page_with_message.html', message='You have successfully registered. Please Log in.')
    return render_template('signup.html', title='Sign Up', form=form)
