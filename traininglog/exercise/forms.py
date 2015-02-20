# forms.py
# Jake Malley
# 01/02/15

"""
Defines the forms to be used regarding exercise data.
"""

# Imports 
from flask_wtf import Form
from wtforms import TextField, SelectField, DecimalField, BooleanField
from wtforms.validators import DataRequired, NumberRange

# DataRequired validator makes sure the data is present in the field.
# NumberRange makes sure the data is between a specific number range.
class AddRunningForm(Form):

    """
    Form for users to add running.
    """

    # Select field for the exercise level.
    exercise_level = SelectField(
        'exercise_type',
        choices=[('1','5 Mph (12 Minute mile)'),
                ('2','6 Mph (10 Minute mile)'),
                ('3','7 Mph (8.5 Minute mile)'),
                ('4','8 Mph (7.5 Minute mile)'),
                ('5','9 Mph (6.5 Minute mile)'),
                ('6','10 Mph (6 Minute mile)')
                ]
    )
    # Decimal field for exercise duration.
    duration = DecimalField(
        'duration',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, max=24)]
    )

class AddCyclingForm(Form):

    """
    Form for users to add cycling.
    """

    # Select field for the exercise level.
    exercise_level = SelectField(
        'exercise_type',
        choices=[('1','< 10 Mph, leisure cycling.'),
                ('2','10 - 11.9 Mph, gentle.'),
                ('3','12 - 13.9 Mph, moderate.'),
                ('4','14 - 15.9 Mph, vigorous.'),
                ('5','16 - 20 Mph, very fast.'),
                ('6','> 20 Mph, racing.')
                ]
    )
    # Decimal field for exercise duration.
    duration = DecimalField(
        'duration',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, max=24)]
    )

class AddSwimmingForm(Form):

    """
    Form for users to add swimming.
    """

    # Select field for the exercise level.
    exercise_level = SelectField(
        'exercise_type',
        choices=[('1','Freestyle, Slow'),
                ('2','Freestyle Fast'),
                ('3','Backstroke'),
                ('4','Breaststroke'),
                ('5','Butterfly')
                ]
    )
    # Decimal field for exercise duration.
    duration = DecimalField(
        'duration',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, max=24)]
    )

class EditExerciseForm(Form):

    """
    Form for users to change the details about their exercise.
    """

    # Hidden field for the exercise id.
    exercise_id = TextField('exercise_id')

    # Decimal field for the new duration.
    duration = DecimalField(
        'duration',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, max=24)]
    )
    # Check box field for users to delete the exercise.
    delete = BooleanField('delete_exercise')


class CompareMemberForm(Form):

    """
    Form for users to select other 
    member to compare with.
    """

    compare_member_1 = SelectField('compare_member_1')
    compare_member_2 = SelectField('compare_member_2')
