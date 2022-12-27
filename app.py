from flask import Flask, Response, send_from_directory, render_template
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def main_view():
    return render_template('index.html')

@app.route('/about')
def about_view():
    return render_template('about.html')

@app.route('/services')
def services_view():
    return render_template('services.html')

@app.route('/service-areas')
def service_areas_view():
    return render_template('service-areas.html')