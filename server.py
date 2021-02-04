# server here
# pip install flask

"""
will probably need sqlite db for image urls
session expires between requests so cant store in memory

"""

from flask import Flask, request
app = Flask(__name__)

IMAGE_URL = None

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/carousel')
def carousel():
    return "carousel template will go here"

@app.route('/addimage', methods=['GET', 'POST'])
def add_image():
    if not request.method == 'POST':
        return('get the fuck outta here that that shit')

    image_url = request.form.get('image_url')
    # probably save the link to a little sqlite db? can't store in mem
    # will need some more methods to grab, sort, etc for the view
    # seed scripts would be sick for local set up
    print(image_url)
    return "got it"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)