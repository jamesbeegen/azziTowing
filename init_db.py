import os
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Normal Connect to the azzitowing database
def db_connect():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = connect(DATABASE_URL, sslmode='require')
    except Exception:
        conn = connect(
            host=os.environ['DATABASE_URL'],
            database="azzitowing",
            user='postgres',
            password='postgres'
        )
    finally:
        return conn

        
# Initializing connect to postgres default database
def init_connect():
    try:
        conn = connect(
                host=os.environ.get('DATABASE_URL'),
                database="postgres",
                user='postgres',
                password='postgres'
        )
    except:
        return None
    else:
        return conn


# Initializes the database
def init_db():
    # Creates tables within the azzitowing database
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS customer;')
    cur.execute('DROP TABLE IF EXISTS service;')
    cur.execute('DROP TABLE IF EXISTS users;')

    # # Create the users table
    # cur.execute("""
    #             CREATE TABLE users(
    #                 username TEXT NOT NULL UNIQUE,
    #                 password NOT NULL UNIQUE
    #             );
    #         """)

    # Create the customer table
    cur.execute("""
                CREATE TABLE customer(
                    email TEXT NOT NULL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
            """)

    # Create the service table
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
                    notes TEXT,
                    payment_link TEXT,
                    checkout_session_id TEXT,
                    approved INT NOT NULL,
                    FOREIGN KEY(customer_email) REFERENCES customer(email)
                );
            """)

    conn.commit()
    conn.close()