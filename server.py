# server here
# pip install flask

import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request, render_template
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME')
SERVER_URL = os.getenv('SERVER_URL')
CAROUSEL_DELAY = os.getenv('CAROUSEL_DELAY')

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/carousel')
def carousel():
    images = get_unseen_images()
    return render_template("carousel.html", title='Carousel', images=images, server_url=SERVER_URL, delay=CAROUSEL_DELAY)

@app.route('/addimage', methods=['GET', 'POST'])
def add_image():
    if not request.method == 'POST':
        return('get the fuck outta here that that shit')

    image_url = request.form.get('image_url')
    print(image_url)

    add_image_to_db(image_url)
    return "Got it", 201

@app.route('/flushqueue', methods=['GET', 'POST'])
def flush_queue():
    if not request.method == 'POST':
        return('get the fuck outta here that that shit for real tho')

    password = request.form.get('hehe')
    if password != 'supersecretpasswordonlythebotknows':
        return "hm"

    empty_queue()
    return "Got it", 200

@app.route('/imageseen', methods=['GET', 'POST'])
def seen_image():
    if not request.method == 'POST':
        return('get the fuck outta here that that shit')

    image_url = request.form.get('image_url')

    skip_image(image_url)
    return "Got it", 201

def get_db_path():
    global DATABASE_NAME
    if not DATABASE_NAME:
        DATABASE_NAME = os.getenv('DATABASE_NAME')
    db_path = '{}/{}.db'.format(os.getcwd(), DATABASE_NAME)
    print(db_path)
    return db_path

def create_connection():
    """ create a database connection to a SQLite database """
    db_file = get_db_path()
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def add_image_to_db(image_url):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO image(url, seen) VALUES(?, 0)', (image_url,))
    conn.commit()
    conn.close()
    return cur.lastrowid

def empty_queue():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('UPDATE image SET seen = 1 WHERE seen = 0')
    conn.commit()
    conn.close()

def skip_image(image_url):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('UPDATE image SET seen = 1 WHERE url = ?', (image_url,))
    conn.commit()
    conn.close()
    return cur.lastrowid

def get_unseen_images():
    # get all the unseen image urls in a list for the carousel handler to pass to template
    image_url_list = []

    conn = create_connection()
    cur = conn.cursor()
    for image in cur.execute('SELECT * from image WHERE seen = 0'):
        image_url_list.append(image[0])
    conn.commit()
    conn.close()
    return image_url_list


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
