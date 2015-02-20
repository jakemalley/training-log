# admin/views.py
# Jake Malley
# 19/02/15

"""
Defines the forms to be used in the admin blueprint.
"""

# Imports 
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# DataRequired validator makes sure the data is present in the field.
# Length validator makes sure the field is between a specific lenght
# EqualTo validator makes sure the field is equal to another field.
# Email validator makes sure the field is a valid email.

class AdminEditDetailsForm(Form):
    """
    Form for admins to edit personal details.
    """

    # Hidden field for the exercise id.
    member_id = TextField('member_id')

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
    # Password field for the password.
    password = PasswordField(
        'password',
        validators=[Length(max=32)]
    )
    # Password field for the password confirm.
    confirm_password = PasswordField(
        'confirm_password',
        validators=[EqualTo('password',message='Passwords must match.')]
    )
    # Boolean Field for setting admin.
    set_admin = BooleanField('admin')
    # Boolean Field for setting active
    set_active = BooleanField('admin')
    # Boolean Field for deleting the user.
    delete_user = BooleanField('delete_user')
