from flask import Flask, g, render_template, request
import sqlite3
app = Flask(__name__)
db_location = 'var/merchisinn.db'

# Database
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        db.cursor().execute('INSERT INTO customers (email, password, first_name, last_name) VALUES ("' + email + '", "' + password + '", "' + firstname + '", "' + surname + '")')
        db.commit()

        test = firstname + surname + email + password
        return test
    else:
        return render_template('register.html')

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
