from datetime import datetime

from string import digits
from random import choice

import pymysql


MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'xY$**QcUMFGujT#C'
MYSQL_PASSWORD = 'k^6(cG+KFDVhF@Hr'
MYSQL_DB = 'btc_wallet'



def create_conn():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )


def create_user_table():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE users(id int UNIQUE NOT NULL,
                    username varchar(50) NOT NULL UNIQUE,
                    email varchar(50) NOT NULL UNIQUE,
                    phone varchar(20) NOT NULL UNIQUE,
                    btc_wallet varchar(40) NOT NULL,
                    password varchar(30) NOT NULL,
                    secure_key varchar(20) NOT NULL
                    )''')
    cursor.close()
    conn.close()

def create_users_finance_table():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE finances(user_id int UNIQUE,
        balance int,
        status int)
    ''')
    cursor.close()
    conn.close()


def create_transactions_table():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE transactions(from varchar(50) NOT NULL,
            to varchar(50) NOT NULL,
            amount int NOT NULL,
            trans_time datetime NOT NULL)
        ''')
    cursor.close()
    conn.close()


def check_user_existence(username, password):
    conn = create_conn()
    cursor = conn.cursor()
    sql_request = cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    cursor.close()
    conn.close()
    return sql_request



def check_email(email):
    conn = create_conn()
    cursor = conn.cursor()
    sql_request = cursor.execute("SELECT email FROM users WHERE email=%s", (email))
    cursor.close()
    conn.close()
    return sql_request


def create_user_account(id, balance, status):
    account = (id, balance, status)
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO finances (user_id, balance, status)
                    VALUES ('%s', '%s', '%s')""" % account)
    cursor.close()
    conn.commit()
    conn.close()


def create_new_user(username, email, phone, btc_wallet, password, secure_key):
    new_user = (generate_user_id(),username, email, phone, btc_wallet, password, secure_key)
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (id, username, email, phone, btc_wallet, password, secure_key) 
                    VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s')""" % new_user)
    cursor.close()
    conn.commit()
    conn.close()
    create_user_account(new_user[0], 0, 0)


def check_wallet_valid(adr):
    validity = False
    if len(adr) >= 26 and len(adr) <= 35:
        validity = True
    else:
        pass

    return validity


def get_user_id(user):
    conn = create_conn()
    cursor = conn.cursor()
    rqst = cursor.execute("SELECT id FROM users WHERE username=%s", (user))

    if rqst != 0:
        result = dict(cursor.fetchone()).get("id", 0)
        return result
    else:
        pass
    cursor.close()
    conn.close()


def get_user_balance(user_id):
    conn = create_conn()
    cursor = conn.cursor()
    rqst = cursor.execute("SELECT balance FROM finances WHERE user_id=%s", (user_id))
    if rqst != 0:
        return dict(cursor.fetchone()).get("balance", 0)
    else:
        pass
    cursor.close()
    conn.close()


def get_user_status(user_id):
    conn = create_conn()
    cursor = conn.cursor()
    rqst = cursor.execute("SELECT status FROM finances WHERE user_id=%s", (user_id))
    if rqst != 0:
        return dict(cursor.fetchone()).get("balance", 0)
    else:
        pass
    cursor.close()
    conn.close()


def get_secure_key(user_id):
    conn = create_conn()
    cursor = conn.cursor()
    rqst = cursor.execute("SELECT secure_key FROM users WHERE id=%d" % user_id)
    if rqst != 0:
        res = cursor.fetchone()['secure_key']
        return res
    else:
        pass
    cursor.close()
    conn.close()
    
def get_user_full_info(user):
    return {"username":user, "user_id":get_user_id(user), "balance":get_user_balance(id), "status": get_user_status(id)}

def check_btc_adrr_validity(addr):
    is_valid = False
    if len(addr) >= 25 and len(addr) <= 35:
        is_valid = True
    else:
        pass
    return is_valid


def generate_user_id():
    result = ""
    for _ in range(0,5):
        result += choice(digits)
    return int(result)

def get_nowtime():
    now_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return now_time

def add_funds(user_id, amount):
    conn = create_conn()
    cursor = conn.cursor()

    sql = "UPDATE finances SET balance = %s WHERE user_id = %s"
    val = (amount, user_id)

    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()


def send_funds():pass




    
    