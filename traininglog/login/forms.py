# login/forms.py
# Jake Malley
# 19/01/15

"""
Defines all the forms used in the login blueprint.
"""

# Imports
from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, DecimalField, BooleanField
from wtforms.validators import StopValidation,DataRequired, Email, Length, EqualTo, NumberRange

# DataRequired validator makes sure the data is present in the field.
# Length validator makes sure the field is between a specific lenght
# EqualTo validator makes sure the field is equal to another field.
# Email validator makes sure the field is a valid email.  
# NumberRange makes sure the data is between a specific number range.

def is_a_float(form, field):
    """
    Validator to check the field is a float.
    """
    print(field.data)
    if field.data is not None:
        try:
            # Try to convert the field to a float.
            float(field.data)
        except ValueError:
            # The field is not a float.
            field.errors[:] = ['Must be a numerical value.']
            # Stop all further validations.
            raise StopValidation()
    else:
        # The field is not a float.
        field.errors[:] = ['This field is required and must be a numerical value.']
        # Stop all further validations.
        raise StopValidation()


class LoginForm(Form):

    """
    Form for users to login to the site.
    """

    # Text field for the users email.
    email = TextField('email',validators=[DataRequired(),Email(message=None),Length(max=50)])
    
    # Password field for the users password.
    password = PasswordField('password',validators=[DataRequired(),Length(max=32)])

    # Remember Me field.
    remember = BooleanField('remember me')

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
        validators=[DataRequired(),Email(message=None),Length(max=50)]
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
        validators=[is_a_float, DataRequired(),NumberRange(min=0,max=3)]
    )
    # Decimal field for the users weight.
    weight = DecimalField(
        'weight',
        places=2,
        validators=[DataRequired(),NumberRange(min=0,max=250)]
    )
    # Text field for the first line of the users address.
    address_line_1 = TextField(
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

class EditDetailsForm(Form):
    """
    Form for users to edit their personal details. 
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
    # Decimal field for the users height.
    height = DecimalField(
        'height',
        places=2,
        validators=[DataRequired(),NumberRange(min=0,max=3)]
    )
    # Text field for the first line of the users address.
    address_line_1 = TextField(
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
    # Password field needed for the user to update their details.
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6,max=32)]
    )

class ChangePasswordForm(Form):
    """
    Form that allows users to change their password.
    """

    # Password field needed for the user to change their password
    current_password = PasswordField(
        'current_password',
        validators=[DataRequired()]
    )
    # Password field for the new password.
    new_password = PasswordField(
        'new_password',
        validators=[DataRequired(), Length(min=6,max=32)]
    )
    # Password field for the new password confirmation.
    new_password_confirm = PasswordField(
        'new_password_confirm',
        validators=[DataRequired(),EqualTo('new_password', message='Passwords must match.')]
    )