# forms.py
# Jake Malley
# 19/01/15

"""
Defines all the forms used in the login blueprint.
"""

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):

    """
    Form for users to login to the site.
    """

    # Text field for the users email.
    email = TextField('email',validators=[DataRequired(),Email(message=None)])
    
    # Password field for the users password.
    password = PasswordField('password',validators=[DataRequired()])
