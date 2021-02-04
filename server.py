# server here
# pip install flask

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/carousel')
def carousel():
    return "carousel template will go here"

@app.route('/addimage', methods=['POST'])
def add_image():
    if not request.method == 'POST':
        return('get the fuck outta here that that shit')

    image_url = request.form.get('image_url')
    print(image_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)