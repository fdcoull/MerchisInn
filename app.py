from flask import Flask, g, render_template, request, session, redirect, url_for
import sqlite3
import configparser
import bcrypt
from functools import wraps

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

# Config
def init(app):
    config = configparser.ConfigParser()
    try:
        print("INIT FUNCTION")
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")
    except:
        print("Could not read configs")

    try:
        print("Load keys")
        keys_location = "etc/key.cfg"
        config.read(keys_location)
        app.config['SECRET_KEY'] = config.get("key", "secret_key")
    except:
        print("Could not read keys")

init(app)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
def account():
    status = session.get('logged_in', False)
    if status:
        email = session.get('user_email')
        if email is not None:
            return render_template('account.html')
        else:
            return redirect(url_for('.logout'))
    else:
        return redirect(url_for('.login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        rows = db.cursor().execute('SELECT password FROM customers WHERE email="' + email + '"').fetchall()
        
        if rows[0][0].encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), rows[0][0].encode('utf-8')):
            
            session['user_email'] = email
            session['logged_in'] = True
            return redirect(url_for('.account'))
        else:
            return redirect(url_for('.login'))
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        passwordHashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        db = get_db()
        db.cursor().execute('INSERT INTO customers (email, password, first_name, last_name) VALUES ("' + email + '", "' + passwordHashed.decode('utf-8') + '", "' + firstname + '", "' + surname + '")')
        db.commit()

        session['user_email'] = email
        session['logged_in'] = True

        test = firstname + surname + email + password
        return test
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_email'] = ""
    return redirect(url_for('.home'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        status = session.get('logged_in', False)

        checkin = request.form['checkin']
        checkout = request.form['checkout']
        guests = request.form['guests']
        beds = request.form['beds']
        accessible = request.form['accessible']

        kings = request.form['kings']
        kingsingles = request.form['kingsingles']
        families = request.form['families']
        familyaccessibles = request.form['familyaccessibles']
        if status:
            db = get_db()

            email = session.get('user_email')

            rows = db.cursor().execute('SELECT id FROM customers WHERE email="' + email + '"').fetchall()
            userid = rows[0][0]

            db.cursor().execute('INSERT INTO bookings (customer_id, check_in, check_out, no_guests, no_beds, no_accessible) VALUES ("' + userid + '", "' + checkin '", "' + checkout + '", ' + guests + ', ' + beds + ', ' + accessible + ')')
        else:
            return redirect(url_for('.login'))
    else:
        return render_template('book.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/getsession')
def getsession():
    email = session.get('user_email')
    if email is not None:
        return 'Email: ' + email
    return 'Not logged in'

@app.route('/delsession')
def delsession():
    session.pop('user_email', None)
    return "Logged out"

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
