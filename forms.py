from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    DateField,
    TimeField,
    SelectField,
    TelField,

)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from flask_login import current_user
from wtforms import validators

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


class login_form(FlaskForm):
    username = StringField(
            validators=[InputRequired()]
        )
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])    

class schedule_form(FlaskForm):
    first_name = StringField('first_name', validators=[InputRequired()])
    last_name = StringField('last_name', validators=[InputRequired()])
    email = EmailField('email', validators=[InputRequired()])
    phone_number = TelField('phone_number', validators=[InputRequired()], id='phoneNumber')
    service_type = SelectField('service_type', validators=[InputRequired()], choices=['Lockout Recovery', 'Fuel Delivery', 'Vehicle Transport', 'Battery Jump'])
    date = DateField('date', validators=[InputRequired()])
    time = SelectField('time', validators=[InputRequired()], choices=generate_time_selections())

class date_schedule_form(FlaskForm):
    date = DateField('date', validators=[InputRequired()])