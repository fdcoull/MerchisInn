from flask import Flask, g, render_template, request, session, redirect, url_for
import sqlite3
import configparser
import bcrypt
from functools import wraps
from datetime import datetime

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
            db = get_db()
            rows = db.cursor().execute('SELECT * from customers WHERE email = "'+ email +'"').fetchall()
            
            bookings = db.cursor().execute('SELECT * from bookings WHERE customer_id = '+ str(rows[0][0])).fetchall()
            return render_template('account.html', email=rows[0][1], firstname=rows[0][3], surname=rows[0][4], bookings=bookings)
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
        return redirect(url_for('.account'))
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

        room = request.form['room']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        guests = request.form['guests']
        accessible = request.form['accessible']


        if status:
            db = get_db()

            email = session.get('user_email')

            if accessible == "":
                accessible == 0

            rows = db.cursor().execute('SELECT id FROM customers WHERE email="' + email + '"').fetchall()
            customerid = rows[0][0]
            
            preorderdifference = datetime.strptime(checkin, '%Y-%m-%d').date() - datetime.now().date()
            preorderdays = preorderdifference.days

            if preorderdays == 0:
                pricemultiplier = 1.5
            elif preorderdays == 1:
                pricemultiplier = 1.25
            else:
                pricemultiplier = 1

            if room == "king":
                #Check king rooms
                rows = db.cursor().execute('SELECT * FROM rooms WHERE (id <= 5 AND id NOT IN (SELECT room_id FROM bookings WHERE check_in<="'+ checkout +'" AND check_out>="'+ checkin +'"))').fetchall()
                
                price = 60 * pricemultiplier

                if len(rows) >= 1:
                    roomid = rows[0][0]
                else:
                    return redirect(url_for('.book', error = "not_available"))

            elif room == "kingsingle":
                #Check king singles
                rows = db.cursor().execute('SELECT * FROM rooms WHERE (id >= 6 AND id <= 7 AND id NOT IN (SELECT room_id FROM bookings WHERE check_in<="'+ checkout +'" AND check_out>="'+ checkin +'"))').fetchall()

                price = 70 * pricemultiplier

                if len(rows) >= 1:
                    roomid = rows[0][0]
                else:
                    return redirect(url_for('.book', error = "not_available"))
            elif room == "family":
                #Check family
                rows = db.cursor().execute('SELECT * FROM rooms WHERE (id >= 8 AND id <= 9 AND id NOT IN (SELECT room_id FROM bookings WHERE check_in<="'+ checkout +'" AND check_out>="'+ checkin +'"))').fetchall()

                price = 80 * pricemultiplier

                if len(rows) >= 1:
                    roomid = rows[0][0]
                else:
                    return redirect(url_for('.book', error = "not_available"))
            elif room == "accessible":
                #Check accessible
                rows = db.cursor().execute('SELECT * FROM rooms WHERE (id == 10 AND id NOT IN (SELECT room_id FROM bookings WHERE check_in<="'+ checkout +'" AND check_out>="'+ checkin +'"))').fetchall()

                price = 80 * pricemultiplier

                if len(rows) >= 1:
                    roomid = rows[0][0]
                else:
                    return redirect(url_for('.book', error = "not_available"))

            else:
                return redirect(url_for('.book'))
            
            staylength = datetime.strptime(checkout, '%Y-%m-%d').date() - datetime.strptime(checkin, '%Y-%m-%d').date()
            staylengthdays = staylength.days

            totalprice = staylengthdays * price
            formattedprice = "%.2f" % totalprice

            db.cursor().execute('INSERT INTO bookings (customer_id, room_id, check_in, check_out, no_guests, accessible, price) VALUES ('+ str(customerid) +', '+ str(roomid) +', "'+ checkin +'", "'+ checkout +'", '+ str(guests) +', '+ str(accessible) +', '+ formattedprice +')')
            db.commit()

            return redirect(url_for('.confirm', room=roomid, checkin=checkin, checkout=checkout, guests=guests, accessible=accessible, price=totalprice))
        else:
            return redirect(url_for('.login'))
    else:
        return render_template('book.html')

@app.route('/confirm')
def confirm():
    room = request.args.get('room', '')
    checkin = request.args.get('checkin', '')
    checkout = request.args.get('checkout', '')
    guests = request.args.get('guests', '')
    accessible = request.args.get('accessible', '')
    price = request.args.get('price', '')
    return render_template('confirm.html', room=room, checkin=checkin, checkout=checkout, guests=guests, accessible=accessible, price=price)

@app.route('/admin')
def admin():
    admin = session.get('admin', False)

    if admin:
        return render_template('admin.html')
    else:
        return redirect(url_for('.adminlogin'))

@app.route('/admin/login', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        print("test")
    else:
        return render_template('admin-login.html')

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
