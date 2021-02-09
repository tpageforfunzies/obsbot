# server here
# pip install flask

"""
will probably need sqlite db for image urls
session expires between requests so cant store in memory

"""
import os
import sqlite3
from sqlite3 import Error
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
def add_image(conn):
    if not request.method == 'POST':
        return('get the fuck outta here that that shit')

    image_url = request.form.get('image_url')
    # probably save the link to a little sqlite db? can't store in mem
    # will need some more methods to grab, sort, etc for the view
    # seed scripts would be sick for local set up
    print(image_url)
    add_image(conn, image_url)
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

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def add_image(image_url):
    global conn
    cur = conn.cursor()
    cur.execute('INSERT INTO image(url, seen) VALUES(?, 0)', (image_url,))
    conn.commit()
    return cur.lastrowid

def skip_image(image_url):
    global conn
    cur = conn.cursor()
    cur.execute('UPDATE image SET seen = 1 where url = image_url')
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':
    cwd = os.getcwd()
    database = cwd + "pythonsqlite.db"
    print(database)
    conn = create_connection(database)
    app.run(host='0.0.0.0', port=80)
