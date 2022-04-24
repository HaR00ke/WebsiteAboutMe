import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_mail import Message, Mail

from config import Config
from .blueprints.confirm_mail_api import confirm_mail_api
from .blueprints.reset_password_api import reset_password_api

app = Flask(__name__, template_folder='templates')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['DEBUG'] = Config.DEBUG_MODE
app.config['PERMANENT_SESSION_LIFETIME'] = Config.PERMANENT_SESSION_LIFETIME
app.config['SECURITY_PASSWORD_SALT'] = Config.SECURITY_PASSWORD_SALT
app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app=app)


def run():
    port = int(os.environ.get("PORT", 5000))
    app.register_blueprint(confirm_mail_api.blueprint)
    app.register_blueprint(reset_password_api.blueprint)
    app.run(host='0.0.0.0', port=port)


def send_mail(to, subject, template):
    print(f'SENDING MAIL TO: {to}, {subject}, {template}')
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    return mail.send(msg)

