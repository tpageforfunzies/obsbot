# server here
# pip install flask

from flask import Flask, request
app = Flask(__name__)

IMAGE_URL = None

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/carousel')
def carousel():
    print(IMAGE_URL)
    if IMAGE_URL != None:
        return "{IMAGE_URL}"
    return "carousel template will go here"

@app.route('/addimage', methods=['POST'])
def add_image():
    if not request.method == 'POST':
        return('get the fuck outta here that that shit')

    image_url = request.form.get('image_url')
    IMAGE_URL = image_url
    print(image_url)
    return "got it"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)