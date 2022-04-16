from .main import app


@app.route('/hi')
def hello():
    return "hello"  
