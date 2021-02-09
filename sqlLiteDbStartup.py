import sqlite3
import os
from sqlite3 import Error

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def main():
    cwd = os.getcwd()
    database = cwd + "pythonsqlite.db"

    sql_create_image_table = """ CREATE TABLE IF NOT EXISTS image(url text PRIMARY KEY, seen integer); """

    conn = create_connection(database)
    with conn:
        create_table(conn, sql_create_image_table)

if __name__ == '__main__':
    main()
