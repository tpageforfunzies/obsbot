# server here
# pip install flask

"""
will probably need sqlite db for image urls
session expires between requests so cant store in memory

"""

from flask import Flask, request, render_template
app = Flask(__name__)

IMAGE_URL = None

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/carousel')
def carousel():
    return render_template("carousel.html")

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

@app.route('/flushqueue', methods=['GET', 'POST'])
def flush_queue():
    if not request.method == 'POST':
        return('get the fuck outta here that that shit for real tho')

    password = request.form.get('hehe')
    if password != 'supersecretpasswordonlythebotknows':
        return "hm"
    # wtf do we do here
    # will probably depend on implementation of db+carousel
    # maybe the image url rows have a seen field and we mark em all seen or something, or just delete them?
    print(password)
    return "got it"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
