import sqlite3

connection = sqlite3.connect('tydzen.db',check_same_thread=False)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER, user_id INTEGER, form TEXT,  name TEXT, score INTEGER, links TEXT, admin INTEGER, tg_username TEXT)")

def get_user(user_id):
    cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    l = cursor.fetchone()
    if(l == None):
        return []
    return l

def get_user_id(id):
    cursor.execute(f"SELECT * FROM users WHERE id={id}")
    l = cursor.fetchone()
    if(l == None):
        return []
    return l


def add_user(user_id,name,form,links,tg_username):
    cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    id = cursor.fetchone()
    # print(id)
    if not id:
        id = 99
    else:
        id = id[0]
    id += 1
    cursor.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?)",(id,user_id,form,name,0, links,0,tg_username))
    connection.commit()
    


def add_admin(user_id):
    cursor.execute(f"UPDATE users SET admin=1 WHERE user_id={user_id}")
    connection.commit()
    # print('here')

def add_points(id,plus):
    cursor.execute(f"SELECT * FROM users WHERE id={id}")
    l = cursor.fetchone()
    # print(l)
    # print(l[4])
    amount = l[4] + plus
    cursor.execute(f"UPDATE users SET score=(?) WHERE id={id}",(amount,))
    connection.commit()

def get_users():
    cursor.execute(f"SELECT * FROM users")
    l = cursor.fetchall()
    if(l == None):
        return []
    return l




cursor.execute("CREATE TABLE IF NOT EXISTS answers(id INTEGER, user_id INTEGER, start INTEGER, end INTEGER, date  TEXT,name TEXT, checked INTEGER)")


def add_answer(id,user_id,start,end,date,name):
    cursor.execute(f"INSERT INTO answers VALUES (?,?,?,?,?,?,?)",(id,user_id,start,end,date,name,0))
    connection.commit()

def get_quest_answer():
    ch = 0
    cursor.execute(f"SELECT * FROM answers WHERE checked=(?)",(0,))
    l = cursor.fetchall()
    if l == None:
        return []
    
    return l

def change_checked(id,start):
    cursor.execute(f"UPDATE answers SET checked=1 WHERE id={id} AND start={start}")
    connection.commit()

def get_answers():
    cursor.execute(f"SELECT * FROM answers")
    l = cursor.fetchall()
    if(l == None):
        return []
    return l