from flask import Flask, g, render_template, request, session
import sqlite3
import configparser

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

@app.route('/test')
def test():
    return app.config['secret_key']

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

        session['user_email'] = email

        test = firstname + surname + email + password
        return test
    else:
        return render_template('register.html')

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
