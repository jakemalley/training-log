# querying_functions.py
# Jake Malley
# 06/02/15

"""
Functions for querying the database.
"""

# Imports
from traininglog.models import Member, Exercise, Weight, Message
from flask.ext.login import current_user

# Querying Functions
def get_exercise_total(date, member=current_user):
    """
    Returns the number of hours exercised on the date given.
    """
    exercise_data = Exercise.query.filter(Exercise.date>date.date()).filter_by(member=member).all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total

def get_hours_running(member=current_user):
    """ 
    Returns the total hours of running.
    """
    exercise_data = Exercise.query.filter_by(member=member,exercise_type='running').all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total

def get_hours_cycling(member=current_user):  
    """ 
    Returns the total hours of cycling.
    """ 
    exercise_data = Exercise.query.filter_by(member=member,exercise_type='cycling').all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total

def get_hours_swimming(member=current_user): 
    """ 
    Returns the total hours of swimming.
    """
    exercise_data = Exercise.query.filter_by(member=member,exercise_type='swimming').all()
    total = 0
    for data in exercise_data:
        total += data.exercise_duration
    return total

def get_cals_total(date, member=current_user):
    """
    Returns the total number of calories burned.
    """
    exercise_data = Exercise.query.filter(Exercise.date>date.date()).filter_by(member=member).all()
    total = 0
    for data in exercise_data:
        total += data.get_calories_burned()
    return total

def get_cals_running(member=current_user):
    """ 
    Returns the total calories burned of running.
    """
    exercise_data = Exercise.query.filter_by(member=member,exercise_type='running').all()
    total = 0
    for data in exercise_data:
        total += data.get_calories_burned()
    return total

def get_cals_cycling(member=current_user):  
    """ 
    Returns the total calories burned of cycling.
    """ 
    exercise_data = Exercise.query.filter_by(member=member,exercise_type='cycling').all()
    total = 0
    for data in exercise_data:
        total += data.get_calories_burned()
    return total

def get_cals_swimming(member=current_user): 
    """ 
    Returns the total calories burned of swimming.
    """
    exercise_data = Exercise.query.filter_by(member=member,exercise_type='swimming').all()
    total = 0
    for data in exercise_data:
        total += data.get_calories_burned()
    return total