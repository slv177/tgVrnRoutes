import sqlite3
from _sqlite3 import Error

def db_create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("sqlite version: ", sqlite3.version)
        # cursor = conn.cursor()
        return conn
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()


def db_commit(connection, command):
    cursor = connection.cursor()
    cursor.execute(command)


def db_close(connection):
    connection.close()


