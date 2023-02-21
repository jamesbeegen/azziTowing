"""
IT493 Project - azziTowing

Authors:
    James Beegen
    Shahzor Khan
    Alex Elson
    Maria Eid
    Hasibur Alam
    Samuel Berhe
    Mehedi Fahad
"""

from flask import Flask, Response, send_from_directory, render_template, request, url_for, redirect
import os
from os import environ
from os.path import exists
from sqlite3 import connect
from init_db import init_db, db_connect
import stripe
import datetime

# App Configuration
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

# Checks for Heroku config var, sets to production mode if it finds DATABASE_URL is populated
if os.environ.get('DATABASE_URL') is not None:
    prod = True
    param_query_symbol = '%s'
else:
    prod = False
    param_query_symbol = '?'
    
# Name of the local testing database file
DB = 'database.db'

# API Key for Stripe payments
stripe_key = 'sk_test_51MZ2KAClce1MywlhOsuuW61sleJa4FX39mSt8bQbmBIGb6i2PVf4jAideajXjKTWUENOjq7jxijtWOWVwtBlDC2q00PPk1A193'


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
    if not prod:
        conn = connect(DB)
    else:
        conn = db_connect()

    cur = conn.cursor()

    cur.execute("SELECT * FROM customer WHERE email = {0}".format(param_query_symbol), (customer_email,))
    
    customer = cur.fetchone()

    conn.commit()
    conn.close()

    if customer is not None:
        return True
    else:
        return False


# Main view / index view
@app.route('/')
def main_view():
    return render_template('index.html')


# Scheduling page / schedule form
@app.route('/schedule', methods=('GET', 'POST'))
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

        # Create the service
        cur.execute("INSERT INTO service (service_type, date, time, completed, balance, paid, customer_email) VALUES ({0},{0},{0},{0},{0},{0},{0})".format(param_query_symbol), (request.form['service_type'], request.form['date'], request.form['time'], '0', '0.00', '0', request.form['email']))
        
        conn.commit()
        conn.close()

        return redirect(url_for('schedule_view'))
    # Regular GET request
    else:
        return render_template('schedule.html')


# Admin view
@app.route('/joeazzi')
def admin_view():
    today = datetime.date.today().strftime('%m-%d-%Y')
    if not prod:
        conn = connect(DB)
        
    else:
        conn = db_connect()

    cur = conn.cursor()

    cur.execute("SELECT service_id, service_type, date, time, first_name, last_name, completed, paid FROM service INNER JOIN customer on customer.email=service.customer_email")
    services = cur.fetchall()

    if not prod:
        services_list = []
        x = 0
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
@app.route('/joeazzi/service', methods=('GET', 'POST'))
def service_ticket_view():
    ticket_num = request.args.get('ticket')
    if request.method == "POST":
        if not prod:
            conn = connect(DB)
        else:
            conn = db_connect()
        cur = conn.cursor()
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

        cur.execute("UPDATE service SET service_type = {0}, date = {0}, time = {0}, completed = {0}, balance = {0}, paid = {0} WHERE service_id = {0}".format(param_query_symbol), (request.form['service_type'], date, time, int(request.form['completed']), balance, int(request.form['paid']), ticket_num,))

        conn.commit()
        conn.close()

        return redirect('/joeazzi/service?ticket={}'.format(ticket_num))
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
@app.route('/joeazzi/service/delete')
def delete_service_ticket():
    ticket_num = request.args.get('ticket')
    if not prod:
        conn = connect(DB)
    else:
        conn = db_connect()
        
    cur = conn.cursor()
    cur.execute("DELETE FROM service WHERE service_id = {0}".format(param_query_symbol), (ticket_num,))

    conn.commit()
    conn.close()

    return redirect('/joeazzi')

@app.route('/joeazzi/create-service', methods=('GET', 'POST'))
def create_service_ticket_view():
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
    else:
        return render_template('create-service.html')

@app.route('/joeazzi/customers', methods=('GET', 'POST'))
def customers_view():
    if not prod:
        conn = connect(DB)
        
    else:
        conn = db_connect()

    cur = conn.cursor()
    cur.execute("SELECT * FROM customer")

    customers = cur.fetchall()

    conn.commit()
    conn.close()

    return render_template('customers.html', customers=customers)

@app.route('/joeazzi/customers/record', methods=('GET', 'POST'))
def customer_record_view():
    customer_id = request.args.get('customer')
    if request.method == 'POST':
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
        cur.execute("UPDATE customer SET first_name={0}, last_name={0}, phone={0} WHERE email={0}".format(param_query_symbol), (first_name, last_name, phone, customer_id,))
        conn.commit()
        conn.close()
        return redirect('/joeazzi/customers/record?customer={}'.format(customer_id))
    else:
        if not prod:
            conn = connect(DB)
            
        else:
            conn = db_connect()

        cur = conn.cursor()
        cur.execute("SELECT email, first_name, last_name, phone FROM customer WHERE email={0}".format(param_query_symbol), (customer_id,))
        customer = cur.fetchone()
        conn.commit()
        conn.close()
        return render_template('customer-record.html', customer=customer)


# Main calling function
if __name__ == '__main__':
    if not exists(DB) or prod:
        create_db()

    # App configuration
    app.run(debug=1,
            host='0.0.0.0',
            port='5000')