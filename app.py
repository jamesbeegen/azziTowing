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

from flask import Flask, Response, send_from_directory, render_template
from os import environ, remove as rm
from os.path import join, exists
from sqlite3 import connect


DB = 'database.db'


# Set up database if it doesn't exist
def create_db():
    with connect(DB) as conn:
        cur = conn.cursor()
        cur.executescript("""
            DROP TABLE IF EXISTS test;
            DROP TABLE IF EXISTS customer;
            DROP TABLE IF EXISTS service;
            DROP TABLE IF EXISTS service_ticket;
            CREATE TABLE test (name TEXT PRIMARY KEY NOT NULL);
            CREATE TABLE customer(
                customer_id INTEGER PRIMARY KEY, 
                first_name TEXT NOT NULL, 
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            );
            CREATE TABLE service(
                service_id INTEGER PRIMARY KEY,
                type TEXT NOT NULL,
                date DATE NOT NULL,
                completed int NOT NULL,
                customer_id INTEGER NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
            );
            CREATE TABLE service_ticket(
                ticket_id INTEGER PRIMARY KEY,
                amount REAL NOT NULL,
                paid int NOT NULL,
                service_id INTEGER NOT NULL,
                FOREIGN KEY(service_id) REFERENCES service(service_id)
            );
        """)

        # This is just random data to show database functionality
        cur.execute("INSERT INTO test (name) VALUES ('testing1')")
        cur.execute("INSERT INTO test (name) VALUES ('testing2')")

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def main_view():
    return render_template('index.html')

@app.route('/schedule')
def schedule_view():
    with connect(DB) as conn:
        cur = conn.cursor()
        results = cur.execute("SELECT * FROM test").fetchall()
    return render_template('schedule.html', results=results)

if __name__ == '__main__':
    if not exists(DB):
        create_db()

    app.run(debug=1,
            host='127.0.0.1',
            port='5000')