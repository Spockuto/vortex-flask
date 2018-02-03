from flask import Flask, render_template, redirect, session, url_for, request, g
import sqlite3
import hashlib
import os

app = Flask(__name__)

def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

def validate(username, password):
    con = sqlite3.connect('static/User.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                        completion=check_password(dbPass, password)
    return completion


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

@app.route('/secret')
def secret():
    if session.get('logged_in'):
        return "You have successfully logged in"
    else:
        return redirect('/')

@app.route('/sess')
def sess():
    session['logged_in'] = False
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
