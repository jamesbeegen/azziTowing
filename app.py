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
from os import environ, remove as rm
from os.path import join, exists
from sqlite3 import connect
import stripe

# Name of the database file
DB = 'database.db'

# API Key for Stripe payments
stripe_key = 'sk_test_51MZ2KAClce1MywlhOsuuW61sleJa4FX39mSt8bQbmBIGb6i2PVf4jAideajXjKTWUENOjq7jxijtWOWVwtBlDC2q00PPk1A193'


# Set up database if it doesn't exist
def create_db():
    with connect(DB) as conn:
        cur = conn.cursor()
        cur.executescript("""
            DROP TABLE IF EXISTS test;
            DROP TABLE IF EXISTS customer;
            DROP TABLE IF EXISTS service;
            DROP TABLE IF EXISTS service_ticket;
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
                balance REAL,
                paid int NOT NULL,
                customer_email INTEGER NOT NULL,
                FOREIGN KEY(customer_email) REFERENCES customer(email)
            );
        """)

def customer_exists(customer_email):
    with connect(DB) as conn:
        cur = conn.cursor()
        customer = cur.execute("SELECT * FROM customer WHERE email = ?", (customer_email,)).fetchone()
    if customer is not None:
        return True
    else:
        return False
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def main_view():
    return render_template('index.html')

@app.route('/schedule', methods=('GET', 'POST'))
def schedule_view():
    # If posting a web form to schedule service:
    if request.method == "POST":
        with connect(DB) as conn:
            cur = conn.cursor()

            # Check if customer exists, create them if not
            if not customer_exists(str(request.form['email'])):
                cur.execute("INSERT INTO customer (first_name, last_name, email, phone) VALUES (?,?,?,?)", (request.form['first_name'], request.form['last_name'], request.form['email'], request.form['phone_number']))

            # Create the service
            cur.execute("INSERT INTO service (service_type, date, time, completed, balance, paid, customer_email) VALUES (?,?,?,?,?,?,?)", (request.form['service_type'], request.form['date'], request.form['time'], '0', '0.00', '0', request.form['email']))

        return redirect(url_for('schedule_view'))

    else:
        with connect(DB) as conn:
            cur = conn.cursor()
            results = cur.execute("SELECT * FROM customer").fetchall()
        return render_template('schedule.html', results=results)

@app.route('/joeazzi')
def admin_view():
    with connect(DB) as conn:
        cur = conn.cursor()
        customers = cur.execute("SELECT * FROM customer").fetchall()
    return render_template('admin.html', customers=customers)

if __name__ == '__main__':
    if not exists(DB):
        create_db()

    app.run(debug=1,
            host='127.0.0.1',
            port='5000')