# from flask_wtf import Form
from flask_wtf import FlaskForm as Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email
from wtforms.validators import Length

class PasswordForm(Form):
    password = PasswordField('Password', validators=[
        Required(u''),
        Length(min=4, message=(u'...definitely too short'))])
