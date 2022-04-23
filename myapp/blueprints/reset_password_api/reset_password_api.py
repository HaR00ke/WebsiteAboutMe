import datetime

from flask import Blueprint, render_template

from myapp.data.db_session import create_session
from myapp.data.db_models import User
from myapp.forms import ForgotPasswordForm
from ..token import confirm_token

blueprint = Blueprint(
    'reset_password',
    __name__,
    template_folder='templates'
)


@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = confirm_token(token)
    if not email:
        return render_template('page_with_message.html', message="The reset password token doesn't exist or expired!")
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('forgot_password.html', title='Reset Password',
                                   form=form, message="Passwords don't match!")

        if len(form.password.data) < 8:
            return render_template('forgot_password.html', title='Sign Up', form=form, message="Password is too short!")

        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        if datetime.datetime.now() - user.modified_date < datetime.timedelta(
                hours=1) and user.modified_date != user.created_date:
            return render_template('forgot_password.html', title='Reset Password',
                                   form=form, message="You already tried to recover your password in the last hour.")

        user.set_password(form.password.data)
        user.set_modified_date()
        db_sess.commit()
        return render_template('page_with_message.html', title='Reset Password',
                               message='Password has been successfully reset!')
    return render_template('forgot_password.html', title='Reset Password', form=form)
