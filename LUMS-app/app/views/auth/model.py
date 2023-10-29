import connect
import mysql.connector
import hashlib, os
from app import SALT_BITS, ITERATION, HASH_MODE, app, HASH_MODE_TOKEN
import datetime
import jwt


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

def user_exists(user_name):
    conn = getCursor()
    query = f"SELECT * FROM users WHERE user_name = '{user_name}'"
    conn.execute(query)
    result = conn.fetchone()
    return True if result else False

def check_password(user_name, pwd):
    conn = getCursor()
    query = f"SELECT salt, pwd FROM users WHERE user_name = '{user_name}'"
    conn.execute(query)
    result = conn.fetchone()
    # print(result)
    salt, hashed_pwd = result
    input_pwd = hashlib.pbkdf2_hmac(HASH_MODE, pwd.encode(), bytes.fromhex(salt), ITERATION).hex()
    print(f'hashed: {hashed_pwd} , input: {input_pwd}')
    return input_pwd == hashed_pwd

def get_user_id_by_username(user_name):
    conn = getCursor()
    query = f"SELECT user_id FROM users WHERE user_name = '{user_name}'"
    conn.execute(query)
    result = conn.fetchone()
    return result[0]

def get_username_by_user_id(user_id):
    conn = getCursor()
    query = f"SELECT user_name FROM users WHERE user_id = {user_id}"
    conn.execute(query)
    result = conn.fetchone()
    return result[0]


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    print("encoding...")
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        res = jwt.encode(
            payload,
            app.secret_key,
            algorithm=HASH_MODE_TOKEN
        )
        print("Token:")
        print(res)


        decoded = jwt.decode(res,app.secret_key, algorithms=[HASH_MODE_TOKEN])
        print("Decoded:")
        print(decoded)

        return res 

    except Exception as e:
        return e

def get_full_name_by_userid(user_id):
    conn = getCursor()
    query = f"SELECT concat(e.first_name, ' ', e.last_name) FROM users AS u LEFT JOIN employee AS e ON u.user_id = e.emp_id WHERE user_id = {user_id}"
    print(query)
    conn.execute(query)
    result = conn.fetchone()
    return result[0]

def get_role_by_userid(user_id):
    conn = getCursor()
    query = f"SELECT role_id FROM users WHERE user_id = {user_id}"
    conn.execute(query)
    result = conn.fetchone()
    return result[0]
    



def get_password(id):
    pass
    

# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
    
# class User(UserMixin):


#     def __init__(self, user_name, active=True):
#         self.user_name = user_name
#         self.active=active

#     def is_active(self):
#         return self.active

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def __repr__(self):
#         return '<User{}>'.format(self.username)
    

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
