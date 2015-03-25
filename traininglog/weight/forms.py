# weight/forms.py
# Jake Malley
# 03/02/15

"""
Defines the forms used in the weight blueprint.
"""

# Imports
from flask_wtf import Form
from wtforms import DecimalField
from wtforms.validators import DataRequired, NumberRange

class AddWeightForm(Form):

    """
    Form for users to add weight.
    """

    # Decimal field for the weight.
    weight = DecimalField('weight', validators=[DataRequired(), NumberRange(min=0,max=200)])