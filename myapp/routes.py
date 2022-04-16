from flask import render_template
from .main import app
from .variables import States


@app.route('/', methods=['GET'])
def main():
    return render_template('about.html', title='Welcome!', current=States.about)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About me', current=States.about)


@app.route('/achievments', methods=['GET'])
def achievments():
    return render_template('achievments.html', title='My Achievments', current=States.achievments)


@app.route('/projects', methods=['GET'])
def projects():
    return render_template('projects.html', title='My Projects', current=States.projects)


@app.route('/contacts', methods=['GET'])
def contacts():
    return render_template('contacts.html', title='My Contacts', current=States.contacts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Log In', current=States.login)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', title='Sign Up', current=States.register)


@app.route('/hi')
def hello():
    return "hello"
