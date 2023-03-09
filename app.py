"""

░█████╗░███████╗███████╗██╗   ████████╗░█████╗░░██╗░░░░░░░██╗██╗███╗░░██╗░██████╗░
██╔══██╗╚════██║╚════██║██    ╚══██╔══╝██╔══██╗░██║░░██╗░░██║██║████╗░██║██╔════╝░
███████║░░███╔═╝░░███╔═╝██║   ░░░██║░░░██║░░██║░╚██╗████╗██╔╝██║██╔██╗██║██║░░██╗░
██╔══██║██╔══╝░░██╔══╝░░██║   ░░░██║░░░██║░░██║░░████╔═████║░██║██║╚████║██║░░╚██╗
██║░░██║███████╗███████╗██║   ░░░██║░░░╚█████╔╝░░╚██╔╝░╚██╔╝░██║██║░╚███║╚██████╔╝
╚═╝░░╚═╝╚══════╝╚══════╝╚═╝   ░░░╚═╝░░░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░

IT493 Project - azziTowing

Authors:
    James Beegen
    Shahzor Khan
    Alex Elson
    Maria Eid
    Hasibur Alam
    Samuel Berhe
    Mehedi Fahad



Important notes:

We will need to use PostgreSQL locally instead of sqlite. I am using PostgreSQL on my laptop, but have added
support for both sqlite and PostgreSQL to make it easier to develop locally. However, it's getting harder to
support both of the environments as the app becomes more complex:

The following code checks to see whether the app is in "Production" or "PostgreSQL" mode:
          
                if os.environ.get('DATABASE_URL') is not None:
                    prod = True
                    param_query_symbol = '%s'
                else:
                    prod = False
                    param_query_symbol = '?'

This sets a corresponding symbol that is injected into SQL queries that parameterizes the query to avoid SQL injection attacks. The symbol is different for SQLite and PostgreSQL, which is why this is needed. IF you are using PostgreSQL locally, all you need to do is set DATABASE_URL in your shell

                Linux:
                        export DATABASE_URL=127.0.0.1
                Windows:
                        set DATABASE_URL=127.0.0.1

The __main__ function checks for "Production" mode, and calls create_db() function to create the Postgres database in local Postgres mode. created_db() references the init.db file, which has additional checks to first try to connect to the Heroku Postgres instance (which is only accessible from within the Heroku container), and fails over to the local Postgres instance. You will likely experience errors here - make sure to set up Postgres with a username of 'postgres' and a password of 'postgres', and leave the ports at the default settings.

You will notice that in each function that interacts with the database, there is a snippet of code like this:

                if not prod:
                    conn = connect(DB)
                else:
                    conn = db_connect()

The connect() function can be traced to the sqlite3 import, and the db_connect() can be traced to the init_db import below. connect() simply connects to the database.db file, and db_connect() actually connects to a postgres database - db_connect() is only run in "Production" / "Postgres" mode in which prod is set to True. It's becoming more burdensome to add this at every interaction with the database, and to have "hotfixes" for shortcomings of sqlite functionality in order to make both environments work.
"""
import os
import stripe
import datetime
import psycopg2
from forms import login_form
from datetime import timedelta
from flask import Flask, render_template, request, url_for, redirect, flash, session
from os.path import exists
from sqlite3 import connect
from sqlalchemy import create_engine
from init_db import init_db, db_connect
from math import ceil
from gmail import send_payment_link_via_email
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash
#from flask_migrate import Migrate
#from flask_migrate import upgrade,migrate,init,stamp
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

# Load environment variables from .env file
# This fails in production, hence the try/except
try:
    load_dotenv()
except:
    pass

# App Configuration
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = 'secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Checks for Heroku config var, sets to production mode if it finds DATABASE_URL is populated
if os.environ.get('DATABASE_URL') is not None:
    prod = True
    param_query_symbol = '%s'
    try:
        db_connect()
    except:
        init_db()
    if os.environ['DATABASE_URL'] == "127.0.0.1":
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/azzitowing"
    else:
        url = os.environ['DATABASE_URL']
        url = url.replace('postgres://', 'postgresql+psycopg2://')
        app.config['SQLALCHEMY_DATABASE_URI'] = url
 
else:
    prod = False
    param_query_symbol = '?'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Starts the login manager
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Start services for authentication
db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def get_id(self):
           return (self.user_id)

    def __repr__(self):
        return '<User %r>' % self.username


#migrate_service = Migrate()
bcrypt = Bcrypt()
login_manager.init_app(app)
db.init_app(app)
#migrate_service.init_app(app, db)
bcrypt.init_app(app)
    
# Enable CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)

# Name of the local testing database file
DB = 'database.db'

app.app_context().push()
#db.create_all()

# migrate database to latest revision
# init()
# stamp()
# migrate()
# upgrade()

# API Key for Stripe payments
stripe_key = os.environ['stripe_key']
stripe.api_key = stripe_key

# Twilio variables
account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
twilio_number = os.environ['twilio_number']
twilio_api_key = os.environ['twilio_api_key']
twilio_api_sid = os.environ['twilio_api_sid']

# Should be Joe's email - but mine for testing
admin_email = os.environ['admin_email']

if not prod:
    try:
        pwd = "password"
        username = "joeazzi"

        newuser = User(
            username=username,
            pwd=bcrypt.generate_password_hash(pwd).decode('utf-8') ,
        )

        db.session.add(newuser)
        db.session.commit()
    except:
        db.session.rollback()


# Set up local database if it doesn't exist
def create_db():
    if not prod:
        with connect(DB) as conn:
            cur = conn.cursor()
            cur.executescript("""
                DROP TABLE IF EXISTS customer;
                DROP TABLE IF EXISTS service;
                CREATE TABLE customer(
                    email TEXT NOT NULL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
                CREATE TABLE service(
                    service_id INTEGER PRIMARY KEY,
                    service_type TEXT NOT NULL,
                    date DATE NOT NULL,
                    time TEXT NOT NULL,
                    completed int NOT NULL,
                    balance REAL NOT NULL,
                    paid int NOT NULL,
                    customer_email INTEGER NOT NULL,
                    notes TEXT,
                    payment_link TEXT,
                    checkout_session_id TEXT,
                    FOREIGN KEY(customer_email) REFERENCES customer(email)
                );
            """)
    else:
        try:
            conn = db_connect()
            cur = conn.cursor()
            cur.execute('SELECT * FROM customer')
        except Exception as e:
            print('exception in init db')
            init_db()
            return redirect('index.html')
        

# Check if a customer exists
def customer_exists(customer_email):
    # Connect to Database
    if not prod:
        conn = connect(DB)
    else:
        conn = db_connect()

    # Get customers that have matching email
    cur = conn.cursor()
    cur.execute("SELECT * FROM customer WHERE email = {0}".format(param_query_symbol), (customer_email,))
    
    # Fetches only one record into a tuple
    customer = cur.fetchone()

    conn.commit()
    conn.close()

    if customer is not None:
        return True
    else:
        return False

# Manages logins
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


# Login route
@app.route("/joeazzi/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                try:
                    login_user(user)
                except:
                    db.session.rollback()
                finally:
                    return redirect(url_for('admin_view'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("login.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
    )


# Logs out user
@app.route("/joeazzi/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Main view / index view
@app.route('/')
def main_view():
    return render_template('index.html')


# Scheduling page / schedule form
@app.route('/schedule', methods=('GET', 'POST'), strict_slashes=False)
def schedule_view():
    # If posting a web form to schedule service:
    if request.method == "POST":
        if not prod:
            conn = connect(DB)
        else:
            conn = db_connect()

        cur = conn.cursor()

        # Check if customer exists, create them if not
        if not customer_exists(request.form['email']):
            cur.execute("INSERT INTO customer (first_name, last_name, email, phone) VALUES ({0},{0},{0},{0})".format(param_query_symbol), (request.form['first_name'], request.form['last_name'], request.form['email'], request.form['phone_number']))

        # Create the service in database
        cur.execute("INSERT INTO service (service_type, date, time, completed, balance, paid, customer_email) VALUES ({0},{0},{0},{0},{0},{0},{0})".format(param_query_symbol), (request.form['service_type'], request.form['date'], request.form['time'], '0', '0.00', '0', request.form['email']))
        
        conn.commit()
        conn.close()

        return redirect(url_for('schedule_view'))

    # Regular GET request
    else:
        return render_template('schedule.html')


# Admin view
@app.route('/joeazzi', strict_slashes=False)
@login_required
def admin_view():
    # Get today's date
    today = datetime.date.today().strftime('%m-%d-%Y')

    # Connect to database
    if not prod:
        conn = connect(DB)
    else:
        conn = db_connect()

    cur = conn.cursor()

    # Get information about services and the customer the service is for
    cur.execute("SELECT service_id, service_type, date, time, first_name, last_name, completed, paid FROM service INNER JOIN customer on customer.email=service.customer_email")
    services = cur.fetchall()

    # This is a fix for sqlite not formatting dates properly
    if not prod:
        services_list = []
        for service in services:
            entry = []
            for item in service:
                entry.append(item)
            services_list.append(entry)
        services = services_list
        for service in services:
            service[2] = datetime.datetime.strptime(service[2], '%Y-%m-%d')

    conn.commit()
    conn.close()
    return render_template('admin.html', services=services, today=today)


# Service ticket view
@app.route('/joeazzi/service', methods=('GET', 'POST'), strict_slashes=False)
@login_required
def service_ticket_view():
    # Retrieves ticket number from the GET parameter in the URL
    ticket_num = request.args.get('ticket')

    # Ran when the form is submitted
    if request.method == "POST":
        if not prod:
            conn = connect(DB)
        else:
            conn = db_connect()

        cur = conn.cursor()

        # Checks for empty values on submission of form, and defaults them back to existing values if they are empty
        if request.form['balance'] == '':
            cur.execute("SELECT balance FROM service WHERE service_id = {0}".format(param_query_symbol), (ticket_num,))
            balance_tuple = cur.fetchone()
            balance = balance_tuple[0]
        else:
            balance = request.form['balance']
        if request.form['date'] == '':
            cur.execute('SELECT date FROM service WHERE service_id = {}'.format(ticket_num))
            date = cur.fetchone()[0]
        else:
            date = request.form['date']
        if request.form['time'] == '':
            cur.execute('SELECT time FROM service WHERE service_id = {}'.format(ticket_num))
            time = cur.fetchone()[0]
        else:
            time = request.form['time']
        if request.form['notes'] == '':
            cur.execute('SELECT notes FROM service WHERE service_id = {}'.format(ticket_num))
            notes = cur.fetchone()[0]
        else:
            notes = request.form['notes']

        # Update the service entry with the data from the form
        cur.execute("UPDATE service SET service_type = {0}, date = {0}, time = {0}, completed = {0}, balance = {0}, paid = {0}, notes = {0}WHERE service_id = {0}".format(param_query_symbol), (request.form['service_type'], date, time, int(request.form['completed']), balance, int(request.form['paid']), notes, ticket_num,))
        
        conn.commit()
        conn.close()
        return redirect('/joeazzi/service?ticket={}'.format(ticket_num))

    # Ran when simply navigating to the service ticket page for a specific service
    else:
        if not prod:
            conn = connect(DB)
        else:
            conn = db_connect()
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM service INNER JOIN customer on customer.email=service.customer_email WHERE service.service_id = {0}".format(param_query_symbol), (ticket_num,))
        service = cur.fetchone()

        conn.commit()
        conn.close()

        return render_template('service-ticket.html', service=service)


# Deleting a service/service ticket
@app.route('/joeazzi/service/delete', strict_slashes=False)
@login_required
def delete_service_ticket():
    # Gets the current ticket number
    ticket_num = request.args.get('ticket')

    # Connect to database
    if not prod:
        conn = connect(DB)
    else:
        conn = db_connect()
        
    cur = conn.cursor()
    cur.execute("DELETE FROM service WHERE service_id = {0}".format(param_query_symbol), (ticket_num,))

    conn.commit()
    conn.close()

    return redirect('/joeazzi')


# Creating a service from admin section
@app.route('/joeazzi/create-service', methods=('GET', 'POST'), strict_slashes=False)
@login_required
def create_service_ticket_view():
    # If the form has been submitted:
    if request.method == 'POST':
        if not prod:
            conn = connect(DB)
        else:
            conn = db_connect()

        cur = conn.cursor()

        # Check if customer exists, create them if not
        if not customer_exists(request.form['email']):
            cur.execute("INSERT INTO customer (first_name, last_name, email, phone) VALUES ({0},{0},{0},{0})".format(param_query_symbol), (request.form['first_name'], request.form['last_name'], request.form['email'], request.form['phone_number']))

        # Create the service
        cur.execute("INSERT INTO service (service_type, date, time, completed, balance, paid, customer_email) VALUES ({0},{0},{0},{0},{0},{0},{0})".format(param_query_symbol), (request.form['service_type'], request.form['date'], request.form['time'], '0', '0.00', '0', request.form['email']))
        
        conn.commit()
        conn.close()

        return redirect(url_for('admin_view'))

    # Regular GET request
    else:
        return render_template('create-service.html')


# View that lists all customers (not services, but customers)
@app.route('/joeazzi/customers', methods=('GET', 'POST'), strict_slashes=False)
@login_required
def customers_view():
    # Connect to database
    if not prod:
        conn = connect(DB)
        
    else:
        conn = db_connect()

    cur = conn.cursor()

    # Get all customer from database
    cur.execute("SELECT * FROM customer")
    customers = cur.fetchall()

    conn.commit()
    conn.close()
    return render_template('customers.html', customers=customers)


# Individual customer records/info pages
@app.route('/joeazzi/customers/record', methods=('GET', 'POST'), strict_slashes=False)
@login_required
def customer_record_view():
    # Get the current customer_id
    customer_id = request.args.get('customer')

    # If a form has been submitted (to update client info)
    if request.method == 'POST':
        # Connect to Database
        if not prod:
            conn = connect(DB)
            
        else:
            conn = db_connect()

        cur = conn.cursor()

        # Check for empty values from the form
        if request.form['first_name'] == '':
            cur.execute("SELECT first_name FROM customer WHERE email = {0}".format(param_query_symbol), (customer_id,))
            first_name = cur.fetchone()[0]
        else:
            first_name = request.form['first_name']
        
        # Check for empty values from the form
        if request.form['last_name'] == '':
            cur.execute("SELECT last_name FROM customer WHERE email = {0}".format(param_query_symbol), (customer_id,))
            last_name = cur.fetchone()[0]
        else:
            last_name = request.form['last_name']

        # Check for empty values from the form
        if request.form['phone'] == '':
            cur.execute("SELECT phone FROM customer WHERE email = {0}".format(param_query_symbol), (customer_id,))
            phone = cur.fetchone()[0]
        else:
            phone = request.form['phone']

        # Updates the customer record with new information submitted in form
        cur.execute("UPDATE customer SET first_name={0}, last_name={0}, phone={0} WHERE email={0}".format(param_query_symbol), (first_name, last_name, phone, customer_id,))

        conn.commit()
        conn.close()
        return redirect('/joeazzi/customers/record?customer={}'.format(customer_id))

    # Regular GET Request
    else:
        if not prod:
            conn = connect(DB)
        else:
            conn = db_connect()

        # Get the customer information based on the primary key 
        cur = conn.cursor()
        cur.execute("SELECT email, first_name, last_name, phone FROM customer WHERE email={0}".format(param_query_symbol), (customer_id,))
        customer = cur.fetchone()

        conn.commit()
        conn.close()
        return render_template('customer-record.html', customer=customer)


# Generates a payment link
@app.route('/joeazzi/service/generatePaymentLink', strict_slashes=False)
@login_required
def generate_payment_link():
    # Get the current ticket number
    ticket_num = request.args.get('ticket')

    # Connect to database
    if not prod:
            conn = connect(DB)
    else:
        conn = db_connect()
    
    cur = conn.cursor()
    cur.execute("SELECT service_type, balance FROM service WHERE service_id={}".format(param_query_symbol), (ticket_num,))
    ticket_details = cur.fetchone()

    # Format the balance for the stripe api
    balance = int(ceil(ticket_details[1])) * 100

    # Create stripe checkout session/url
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': ticket_details[0],
                    },
                    'unit_amount': balance,
                    'currency': 'usd',
                },
                'quantity': 1,
            },
        ],
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + 'payment/success',
        cancel_url=request.host_url + 'payment/cancel',
    )

    # Update service ticket with payment link
    cur.execute("UPDATE service SET payment_link={0} WHERE service_id={0}".format(param_query_symbol), (checkout_session.url, ticket_num,))

    conn.commit()
    conn.close()

    return redirect('/joeazzi/service?ticket={}'.format(ticket_num))


# Sends payment link via text
@app.route('/joeazzi/sendPaymentLink', strict_slashes=False)
@login_required
def send_payment_link():
    # Twilio client
    client = Client(account_sid, auth_token)

    # Get the current ticket number
    ticket_num = request.args.get('ticket')

    # Connect to database
    if not prod:
            conn = connect(DB)
    else:
        conn = db_connect()
    
    # Retrieve service information
    cur = conn.cursor()
    cur.execute("SELECT phone, email, payment_link, first_name FROM service INNER JOIN customer on customer.email=service.customer_email WHERE service.service_id = {0}".format(param_query_symbol), (ticket_num,))
    service = cur.fetchone()
    conn.commit()
    conn.close()

    # Send the message
    message = client.messages.create(
    body='Hello {}, you need to buy a number before links can be sent'.format(service[3]),
    from_=twilio_number,
    to="+1{}".format(service[0])
    )

    send_payment_link_via_email(admin_email, service[1], service[3], service[2])
    
    return redirect('/joeazzi/service?ticket={}'.format(ticket_num))


# Shows when payment is successful
@app.route('/payment/success', strict_slashes=False)
def success():
    return render_template('success.html')


# Shown when order/payment is cancelled
@app.route('/payment/cancel', strict_slashes=False)
def cancel():
    return render_template('cancel.html')


# Main calling function
if __name__ == '__main__':
    if not exists(DB) or prod:
        create_db()

    # App configuration
    app.run(debug=1,
            host='0.0.0.0',
            port='5000')