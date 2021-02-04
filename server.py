# server here
# pip install flask

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/carousel')
def hello():
    return "carousel template will go here"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)