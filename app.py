from flask import Flask, Response, send_from_directory, render_template
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def main_view():
    return render_template('index.html')
