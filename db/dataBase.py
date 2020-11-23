import numpy as np
import sqlite3

def execute_once():
    connection = sqlite3.connect('./db/database.db')
    with open('./db/schema.sql') as f:
        connection.executescript(f.read())

    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (user, pass) VALUES (?, ?)",
                ('user', 'password'))

    connection.commit()
    connection.close()
    print('Default user added')

def get_connection():
    connection = None
    try:
        connection = sqlite3.connect('./db/database.db')
    except Exception as e:
        print(e)

    return connection

def checkUser(username=None, password=None):
    if username is None or password is None:
        return False
    username = username.lower().strip()
    password = password.lower().strip()
    status = False
    useDB = True #set it to false, if don't want to use db
    if useDB == False:
        if username == 'user' and password == 'password':
            status = True
    else:
        try:
            conn = get_connection()
            with conn:
                cursor = conn.cursor()
                query = cursor.execute("SELECT * FROM users WHERE user=? AND pass=?", (username, password))
                users = query.fetchall()
                print('users ', np.shape(users))
                if len(users)>=1:
                    status = True
            conn.close()
        except Exception as e:
            print(e)
            status = False
            print('checkUser error occured') #handle it later

    return status