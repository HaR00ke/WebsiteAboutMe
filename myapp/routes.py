from flask import render_template, url_for

from .main import app
from .variables import States
from .data.db_models import Project, Achievment, Contact
from .data import db_session


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


@app.route('/comments')
def comments():
    return render_template('comments.html', title='Comments', current=States.comments)


@app.route('/hi')
def hello():
    db_sess = db_session.create_session()
    p = Project()
    p.title = 'Amogus'
    p.description = 'Amogus1123'
    p.url = 'https://youtube.com'
    db_sess.add(p)
    db_sess.commit()
    return "hello"
