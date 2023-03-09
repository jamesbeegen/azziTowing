from wtforms import (
    StringField,
    PasswordField,
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