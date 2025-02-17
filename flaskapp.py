from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(_name_)

# Ensure the database schema is correct
def init_db():
    conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return redirect(url_for('profile', username=username))
    else:
        return "Invalid credentials. Please try again."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        address = request.form['address']

        conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, firstname, lastname, email, address) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, password, firstname, lastname, email, address))
        conn.commit()
        conn.close()

        return redirect(url_for('profile', username=username))

    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)

if _name_ == '_main_':
    app.run(debug=True)