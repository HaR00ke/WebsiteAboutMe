from flask import render_template
from flask_login import login_required, current_user
from datetime import datetime

from .main import app
from .variables import States
from .data.db_models import Project, Achievment, Contact, Comment, User
from .data import db_session
from .forms import EditProfileForm, CommentForm


# ERROR HANDLERS
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def error404(e):
    return render_template('page_with_message.html', title=f'{e.code}', message=e, error=True), e.code


# PAGE ROUTES
@app.route('/', methods=['GET'])
def main():
    return render_template('about.html', title='Welcome!', current=States.about)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About me', current=States.about)


@app.route('/achievments', methods=['GET'])
def achievments():
    db_sess = db_session.create_session()
    list_ = [i.get_dict() for i in db_sess.query(Achievment).all()]
    return render_template('achievments.html', title='My Achievments', current=States.achievments, list_=list_)


@app.route('/projects', methods=['GET'])
def projects():
    db_sess = db_session.create_session()
    list_of_projects = [i.get_dict() for i in db_sess.query(Project).all()]
    return render_template('projects.html', title='My Projects', current=States.projects, list_=list_of_projects)


@app.route('/contacts', methods=['GET'])
def contacts():
    db_sess = db_session.create_session()
    list_ = [i.get_dict() for i in db_sess.query(Contact).all()]
    return render_template('contacts.html', title='My Contacts', current=States.contacts, list_=list_)


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    form = CommentForm()
    db_sess = db_session.create_session()
    list_ = [i.get_dict() for i in db_sess.query(Comment).all()]

    if form.is_submitted():
        x = len(form.text.data)
        if not current_user.is_authenticated:
            return "Ha-Ha, u must be logged in to do that, u stupid kid haha"

        if not current_user.can_comment:
            return render_template('comments.html', title='Comments', current=States.comments, form=form,
                                   message='Oops, u cant comment! Admin banned you!', list_=list_)
        if current_user.comments:
            if (datetime.now() - current_user.comments[0].created_date).total_seconds() < 1800 and not current_user.admin:
                return render_template('comments.html', title='Comments', current=States.comments, form=form,
                                       message="You have already sent a comment in the last hour. Try it after a while",
                                       list_=list_)

        if x < 10:
            return render_template('comments.html', title='Comments', current=States.comments, form=form,
                                   message='Comment is too short!', list_=list_)
        if x > 500:
            return render_template('comments.html', title='Comments', current=States.comments, form=form,
                                   message='Comment  is too long!', list_=list_)
        comment = Comment()
        comment.text = form.text.data
        comment.author_id = current_user.id
        db_sess.add(comment)
        db_sess.commit()

    list_ = [i.get_dict() for i in db_sess.query(Comment).all()]
    return render_template('comments.html', title='Comments', current=States.comments, form=form, list_=list_)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            if (datetime.now() - current_user.modified_date).total_seconds() < 3600 and \
                    current_user.modified_date != current_user.created_date:
                return render_template('profile.html', title='Profile',
                                       message="Your account details have already changed in the"
                                               " last hour. Try after a while.", form=form)
            if not 4 <= len(form.nickname.data) <= 20:
                return render_template('profile.html', title='Sign Up',
                                       form=form, message="The length of the nickname must be between 4 and 20!")
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == current_user.email).first()
            user.email = form.email.data
            user.nickname = form.nickname.data
            user.set_modified_date()
            db_sess.commit()

            return render_template('page_with_message.html', title=f'Changed!',
                                   message='Profile has been successfully edited!')
        return render_template('profile.html', title='Profile', message="Invalid password", form=form)
    form.email.data = current_user.email
    form.nickname.data = current_user.nickname
    return render_template('profile.html', title='Profile', current=States.profile, form=form)

# @app.route('/hi')
# def hello():
#     db_sess = db_session.create_session()
#     p = Project()
#     p.title = 'Amogus'
#     p.description = 'Amogus1123'
#     p.url = 'https://youtube.com'
#     db_sess.add(p)
#     db_sess.commit()
#     return "hello"
