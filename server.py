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

app = Flask(__name__)

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
    # wtf do we do here
    # will probably depend on implementation of db+carousel
    # maybe the image url rows have a seen field and we mark em all seen or something, or just delete them?
    print(password)
    return "Got it", 200

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

def skip_image(image_url):
    global conn
    cur = conn.cursor()
    cur.execute('UPDATE image SET seen = 1 where url = image_url')
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
