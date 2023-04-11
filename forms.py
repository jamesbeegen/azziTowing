from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    DateField,
    TimeField,
    SelectField,
    TelField,
    TextAreaField

)
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from flask_login import current_user
from wtforms import validators

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
    service_type = SelectField('service_type', validators=[InputRequired()], choices=['Lockout Recovery', 'Fuel Delivery', 'Vehicle Transport', 'Battery Jump', 'Emergency Roadside Assistance'])
    date = DateField('date', validators=[InputRequired()])
    time = SelectField('time', validators=[InputRequired()], choices=[])
    notes = TextAreaField('notes')
        

class date_schedule_form(FlaskForm):
    date = DateField('date', validators=[InputRequired()])


class forgot_password_form(FlaskForm):
    email = EmailField('email', validators=[InputRequired()])


class change_password_form(FlaskForm):
    pwd = PasswordField(validators=[InputRequired()])
    confirm_pwd = PasswordField(validators=[InputRequired()])