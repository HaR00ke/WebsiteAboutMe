from flask import render_template, url_for
from .main import app, send_mail
from .variables import States


@app.route('/', methods=['GET'])
def main():
    return render_template('about.html', title='Welcome!', current=States.about)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About me', current=States.about)


@app.route('/achievments', methods=['GET'])
def achievments():
    # [img, title, description, url(optional)]
    list_ = [[url_for('static', filename='img/logo.png'), '1st', 'amogus amogus amogus amogus amogusamogus ', "https://google.com"],
             [url_for('static', filename='img/logo.png'), '1st', 'amogus amogus22'],
             [url_for('static', filename='img/logo.png'), '1st', 'amogus amogus2233'],
             [url_for('static', filename='img/logo.png'), '1st', 'amogus amogus2212312']]
    #TODO: Если очень много текста укоротить... Контролировать размер файла. Недостающие места добавлять пустыми местами
    return render_template('achievments.html', title='My Achievments', current=States.achievments, list_=list_)


@app.route('/projects', methods=['GET'])
def projects():
    return render_template('projects.html', title='My Projects', current=States.projects)


@app.route('/contacts', methods=['GET'])
def contacts():
    # [['button text', 'url']]
    list_ = [['instagram', 'https://instagram.com/haroke4'],
             ['github', 'https://github.com/HaR00ke']]
    return render_template('contacts.html', title='My Contacts', current=States.contacts, list_=list_)


@app.route('/hi')
def hello():
    return "hello"
