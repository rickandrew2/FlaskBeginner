from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with open('db.sql', 'r') as f:
                db.executescript(f.read())
            db.commit()

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def home():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        db.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)', 
                   (name, email, password_hash))
        db.commit()
        return redirect(url_for('home'))
    
    cur = db.execute('SELECT * FROM users')
    users = cur.fetchall()
    return render_template('home.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
