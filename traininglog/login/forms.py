# forms.py
# Jake Malley
# 19/01/15

"""
Defines all the forms used in the login blueprint.
"""

# Imports
from flask_wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class LoginForm(Form):

    """
    Form for users to login to the site.
    """

    # Text field for the users email.
    email = TextField('email',validators=[DataRequired(),Email(message=None)])
    
    # Password field for the users password.
    password = PasswordField('password',validators=[DataRequired(),Length(min=6,max=32)])

class SignUpForm(Form):

    """
    Form for users to signup to the site.
    """ 

    # Text field for the users firstname.
    firstname = TextField(
        'firstname', 
        validators=[DataRequired(),Length(min=2,max=20)]
    )
    # Text field for the users surname.
    surname = TextField(
        'surname', 
        validators=[DataRequired(), Length(min=2,max=20)]
    )
    # Text field for the users email.
    email = TextField(
        'email',
        validators=[DataRequired(),Email(message=None)]
    )
    # Password field for the users chosen password.
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6,max=32)]
    )
    # Password confirmation field.
    password_confirm = PasswordField(
        'password confirmation',
        validators=[DataRequired(),EqualTo('password', message='Passwords must match.')]
    )
    # Select field for selecting gender.
    gender = SelectField(
        'gender', 
        choices=[('male','Male'),('female','Female')]
    )
    # Decimal field for the users height.
    height = DecimalField(
        'height',
        places=2,
        validators=[DataRequired(),NumberRange(min=0,max=3)]
    )
    # Text field for the first line of the users address.
    address_line_1 = TextAreaField(
        'address',
        validators=[DataRequired(),Length(min=5, max=200)]
    )
    # Text field for the users city.
    city = TextField(
        'city',
        validators=[DataRequired(),Length(min=2, max=20)]
    )
    # Text field for the users postcode.
    postcode = TextField(
        'postcode',
        validators=[DataRequired(),Length(min=5,max=9)]
    )
















