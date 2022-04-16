from flask import Flask

import config

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config["DEBUG"] = config.DEBUG_MODE


def run():
    app.run(host='0.0.0.0')
