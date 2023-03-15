from flask import Flask, Response, send_from_directory, render_template, request, url_for, redirect
import os
from os import environ
from os.path import exists
from sqlite3 import connect
from init_db import init_db, db_connect
import stripe
from math import ceil
import datetime
from email.mime.text import MIMEText

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
stripe.api_key = stripe_key

# Should be Joe's email - but mine for testing
admin_email = 'jamesbeegen@gmail.com'


# Checks for proper payment link generation
def proper_payment_link_generation():

    # Create stripe checkout session/url
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': 'test',
                    },
                    'unit_amount': 500,
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

    print(checkout_session)

def send_text():
    import os
    from twilio.rest import Client

    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    account_sid = "ACadd2746c5cb537ea87c10696f1bcbb7d"
    auth_token = "714d7c4cb72f2f41805f11a7e004864b"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    body="Hello from Twilio",
    from_="+18339643387",
    to="+15712718255"
    )

    print(message.sid)

def send_payment_link(link, customer_email, first_name):
    body = """
Hi, {}! Thanks for choosing Azzi Towing. Please use the link below to pay your invoice:
    
{}

Thank you!
""".format(first_name, link)

def replace_heroku_database_url(url):
    return url.replace('postgres://', 'postgresql+psycopg2://')


def generate_time_selections():
    times = []
    for hour in range(0, 23, 2):
        if hour < 12:
            if hour == 0:
                times.append('12:00AM - 2:00AM')
            elif hour == 10:
                times.append('{}:00AM - {}:00PM'.format(hour%12, hour%12+2))
            else:
                times.append('{}:00AM - {}:00AM'.format(hour%12, hour%12+2))
        else:
            if hour == 12:
                times.append('12:00PM - 2:00PM')
            elif hour == 22:
                times.append('{}:00PM - 11:59PM'.format(hour%12))
            else:
                times.append('{}:00PM - {}:00PM'.format(hour%12, hour%12+2))
    return times

def generate_time_selections():
    times = []
    for hour in range(0, 23, 2):
        if hour < 12:
            if hour == 0:
                times.append('12:00AM - 2:00AM')
            elif hour == 10:
                times.append('{}:00AM - {}:00PM'.format(hour%12, hour%12+2))
            else:
                times.append('{}:00AM - {}:00AM'.format(hour%12, hour%12+2))
        else:
            if hour == 12:
                times.append('12:00PM - 2:00PM')
            elif hour == 22:
                times.append('{}:00PM - 11:59PM'.format(hour%12))
            else:
                times.append('{}:00PM - {}:00PM'.format(hour%12, hour%12+2))
    return times


def get_available_time_slots(date):
    print(date)
    all_slots = generate_time_selections()
    available_slots = []

    # Connect to Database
    if not prod:
        conn = connect(DB)
    else:
        conn = db_connect()
    
    cur = conn.cursor()
    cur.execute("SELECT time FROM service WHERE date={}".format(param_query_symbol), (date,))
    taken_times = cur.fetchall()

    conn.commit()
    conn.close()

    for slot in all_slots:
        slot_taken = False
        for taken_time in taken_times:
            if slot in taken_time:
                slot_taken = True
                continue
        if not slot_taken:
            available_slots.append(slot)

    return available_slots

if __name__ == '__main__':
    #proper_payment_link_generation()
    #send_text()
    #send_payment_link('http://google.com', 'jamesbeegen@gmail.com', 'James')
    # heroku_url = 'postgres://ukcuivpnhjuepm:72d2e70507a80420168396ce6cfc3a0596d30e3ee4e8d4a5af70814f431ca001@ec2-3-229-161-70.compute-1.amazonaws.com:5432/d7d24rcph51e21'
    # new_heroku_url = replace_heroku_database_url(heroku_url)
    # print(new_heroku_url)
    times = get_available_time_slots('2023-03-15')
    print(times)
    #for time in times: print(time)