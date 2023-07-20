import flask
from flask import Flask, jsonify, request
import psycopg2


def db_conn():
    return psycopg2.connect(
    host="localhost",
    database="postgresDB",
    user="postgresUser",
    password="postgresPW",
    port=5432)




def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE SCHEMA IF NOT EXISTS schema2;
        """,
        """
        DROP TABLE IF EXISTS schema2.people;
        """,
        """CREATE TABLE schema2.people 
        (user_id serial PRIMARY KEY,
        username VARCHAR ( 300 ) UNIQUE NOT NULL, password VARCHAR ( 300 ) NOT NULL)"""
        ]
    conn = None
    try:
    # connect to the PostgreSQL server
        conn = db_conn()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print("create_tables done")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_user(username, password):
    """ insert a new user into the User table """
    sql = """INSERT INTO schema2.people(username,password)
             VALUES(%s,%s) RETURNING username;"""
    conn = None
    user_id = None
    # try:
    # connect to the PostgreSQL database
    conn = db_conn()
    # create a new cursor
    cur = conn.cursor()
    # execute the INSERT statement
    cur.execute(sql, (username, password))
    # get the generated id back
    user_id = cur.fetchone()[0]
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    return user_id


def get_user(username):
    """ query data from the User table """
    conn = None
    # try:
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM schema2.people WHERE username=%s""", (username,))
    row = cur.fetchone()
    return row
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
# users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    tmpuser = get_user(email)
    if tmpuser is None:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    tmpUser = get_user(email)
    if not tmpUser:
        return
    user = User()
    user.id = email
    return user

# curl -i -X POST -H 'Content-Type: application/json' -d '{"email": "New item", "password": "2009"}' http://127.0.0.1:5000/register
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    tmpUser = get_user(email)
    print(tmpUser, data['password'])
    if tmpUser and data['password'] == tmpUser[2]:
        user = User()
        user.id = email
        flask_login.login_user(user)
        # return flask.redirect(flask.url_for('protected'))
        res = f"login success for {email}"
        return res
    return f'\nBad login {tmpUser} vs {data["password"]} \n'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    tmpUser = get_user(email)
    if not tmpUser:
        insert_user(email, data['password'])
        return f"succedded to register {email}"
    return 'Email already used'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@app.route("/init", methods=["POST"])
def init():
    create_tables()
    return "init done"

if __name__ == '__main__':
    # create_tables()
    # print(insert_user("test1", "test"))
    # print(get_user("123"))
    app.run(debug=True)
