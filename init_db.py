import os
from os import environ
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Normal Connect to the azzitowing database
def db_connect():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
            
    except KeyError:
        conn = connect(
            host=os.environ.get('DATABASE_URL'),
            database="azzitowing",
            user='postgres',
            password='postgres'
        )

        return conn

    else:
        conn = connect(DATABASE_URL, sslmode='require')
        return conn

        
# Initializing connect to postgres default database
def init_connect():
    conn = connect(
            host=os.environ.get('DATABASE_URL'),
            database="postgres",
            user='postgres',
            password='postgres'
    )

    return conn


# Initializes the database
def init_db():
    # Initializing connection to create azzitowing database
    if os.environ.get('HEROKU') != 'true':
        conn = init_connect()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute('CREATE DATABASE azzitowing')
        conn.close()

    # Creates tables within the azzitowing database
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS customer;')
    cur.execute('DROP TABLE IF EXISTS service;')
    cur.execute("""
                CREATE TABLE customer(
                    email TEXT NOT NULL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
            """)

    cur.execute("""
                CREATE TABLE service(
                    service_id SERIAL PRIMARY KEY,
                    service_type TEXT NOT NULL,
                    date DATE NOT NULL,
                    time TEXT NOT NULL,
                    completed INT NOT NULL,
                    balance NUMERIC(7,2) NOT NULL,
                    paid INT NOT NULL,
                    customer_email TEXT NOT NULL,
                    FOREIGN KEY(customer_email) REFERENCES customer(email)
                );
            """)

    conn.commit()
    conn.close()