# models.py
# Jake Malley
# 23/01/2015

"""
Models (Tables) for the database.
"""

# Imports
from traininglog import db
from traininglog import bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class RunningLookUp(db.Model):

    """
    LookUp Table for running.
    """
    # The table name.
    __tablename__ = "RunningLookUp"
    # Table fields.
    id = db.Column(db.Integer,primary_key=True)
    calories_burned = db.Column(db.Integer, nullable=False)

    def __init__(self, id, calories_burned):

        self.id = id
        self.calories_burned = calories_burned

class CyclingLookUp(db.Model):

    """
    LookUp Table for cycling.
    """
    # The table name.
    __tablename__ = "CyclingLookUp"
    # Table fields.
    id = db.Column(db.Integer,primary_key=True)
    calories_burned = db.Column(db.Integer, nullable=False)

    def __init__(self, id, calories_burned):

        self.id = id
        self.calories_burned = calories_burned

class SwimmingLookUp(db.Model):

    """
    LookUp Table for swimming.
    """
    # The table name.
    __tablename__ = "SwimmingLookUp"
    # Table fields.
    id = db.Column(db.Integer,primary_key=True)
    calories_burned = db.Column(db.Integer, nullable=False)

    def __init__(self, id, calories_burned):

        self.id = id
        self.calories_burned = calories_burned

class Message(db.Model):

    """
    Entity to store the messages.
    """

    # The table name.
    __tablename__ = "Message"
    # The table fields.
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    message_text = db.Column(db.String, nullable=False)
    member_id = db.Column(db.Integer, ForeignKey('Member.id'))

    def __init__(self, date, message_text, member_id):

        self.date=date
        self.message_text=message_text
        self.member_id=member_id

    def get_message(self):
        """
        Returns the message text.
        """
        return self.message_text

    def get_date_str(self):
        """
        Returns the date.
        """
        return str(self.date.strftime("%d-%m-%y"))

class Weight(db.Model):

    """
    Entity for all the weight data.
    """

    # The table name.
    __tablename__ = "Weight"
    # Table fields.
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    member_id = db.Column(db.Integer, ForeignKey('Member.id'))

    def __init__(self, weight, date, member_id):

        self.weight=weight
        self.member_id=member_id
        self.date=date

    # Get methods.
    def get_weight(self):
        """
        Returns the weight as a float.
        """
        return float(self.weight)

    def get_date(self):
        """
        Returns the date.
        """
        return self.date.strftime("%d-%m-%y")

    def get_date_str(self):
        """
        Returns the date.
        """
        return str(self.date.strftime("%d-%m-%y"))

    def get_member(self):
        """
        Returns the member object.
        """
        return self.member


class Exercise(db.Model):
    
    """
    Entity for all the exercise data.
    """

    # The table name.
    __tablename__ = "Exercise"
    # Table fields.
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    exercise_type = db.Column(db.Enum('running', 'cycling', 'swimming', name='exercise_type'))
    exercise_level = db.Column(db.Integer, nullable=False)
    exercise_duration = db.Column(db.Float, nullable=False)
    calories_burned = db.Column(db.Float, nullable=False)
    member_id = db.Column(db.Integer, ForeignKey('Member.id'))

    def __init__(self, date, exercise_type, exercise_level, exercise_duration, calories_burned, member_id):

        self.date=date
        self.exercise_type=exercise_type
        self.exercise_level=exercise_level
        self.exercise_duration=exercise_duration
        self.calories_burned=calories_burned
        self.member_id=member_id

    # Get methods.
    def get_member_name(self):
        """
        Returns the full name of the member.
        """
        return self.member.get_full_name()

    def get_member(self):
        """
        Returns the member object.
        """
        return self.member

    def get_exercise(self):
        """
        Returns the exercise_type.
        """
        return self.exercise_type.title()

    def get_datetime(self):
        """
        Returns a string of the date and time.
        """
        return str(self.date.strftime("%d-%m-%y %H:%M"))

    def get_date(self):
        """
        Returns the date.
        """
        return self.date.strftime("%d-%m-%y")

    def get_calories_burned(self):
        """
        Returns the calories_burned.
        """
        return self.calories_burned

    def update_duration(self, new_duration, new_calories_burned):
        """
        Updates the duration and calories_burned for an exercise event.
        """

        # Update the values.
        self.calories_burned=new_calories_burned
        self.exercise_duration=new_duration
        # Commit the changes.
        db.session.commit()

class Member(db.Model):

    """
    Entity for the member's personal details.
    """
    # The table name.
    __tablename__ = "Member"
    # Table fields.
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.Enum('male', 'female', name='gender'))
    height = db.Column(db.Float, nullable=False)
    address_line_1 = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    join_date = db.Column(db.DateTime, nullable=False)
    last_login_date = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    account_is_active = db.Column(db.Boolean, nullable=False)
    # Relationship for exercise.
    exercise_data = relationship("Exercise", backref="member")
    weight_data = relationship("Weight", backref="member")
    message_data = relationship("Message", backref="member")

    def __init__(self, firstname, surname, email, password, gender, height, address_line_1, city, postcode, join_date, last_login_date, is_admin=0, account_is_active=1):
        
        """
        Constructor sets all the fields in the databased based on the parameters.
        """
        self.firstname=firstname.lower()
        self.surname=surname.lower()
        self.email=email.lower()
        # Hash the password
        self.password=bcrypt.generate_password_hash(password)
        self.gender=gender
        self.height=height
        self.address_line_1=address_line_1.lower()
        self.city=city.lower()
        self.postcode=postcode.upper().replace(" ","")
        self.join_date=join_date
        self.last_login_date=last_login_date
        self.is_admin=is_admin
        self.account_is_active=account_is_active

    # Methods for Flask-Login
    def is_authenticated(self):
        """
        Returns true as if there is a user object they are authenticated.
        """
        return True

    def is_active(self):
        """
        Checks the user is active. (Thus allowed to login.)
        """
        return bool(self.account_is_active)

    def is_anonymous(self):
        """
        Used in flask-login. The user is never anonymous always return False.
        """ 
        return False

    def is_administrator(self):
        """
        Returns true if the account has admin privileges.
        """
        return bool(self.is_admin)   

    def set_active_status(self, status=1):
        """
        Sets the status of the account.
        1 = active
        0 = deactivate
        """
        self.account_is_active=status  

    # Get Methods.
    def get_id(self):
        """
        Returns the user's id.
        """
        return unicode(self.id)

    def get_full_name(self):
        """
        Returns the users full name in a title format.
        """
        return self.firstname.title() + " " + self.surname.title()

    def get_firstname(self):
        """
        Returns the users firstname in a title format.
        """
        return self.firstname.title()

    def get_surname(self):
        """
        Returns the users surname in a title format.
        """
        return self.surname.title()

    def get_email(self):
        """
        Returns the email all in lower case.
        """
        return self.email.lower()

    def get_gender(self):
        """
        Returns the gender in a title format.
        """
        return self.gender.title()

    def get_height(self):
        """
        Returns the height.
        """
        return self.height

    def get_address(self):
        """
        Returns a string of the full address.
        """
        return self.address_line_1.title() + ", " + self.city.title() + ", " + self.postcode.upper()

    def get_join_date(self):
        """
        Returns the date the user joined.
        In the format DD MM YYYY HH:MM
        """
        return self.join_date.strftime("%d-%m-%y %H:%M")

    def get_last_login_date(self):
        """
        Returns the date the user last logged in.
        In the format DD MM YYYY HH:MM
        """
        return self.last_login_date.strftime("%d-%m-%y %H:%M")

    # Set Methods.
    def set_last_login_date(self,last_login_date):
        """
        Updates the date of the users last login.
        """
        self.last_login_date=last_login_date

    def update_details(self, firstname, surname, email, height, address_line_1, city, postcode):
        """
        Updates the users details to the details given.
        """
        print("UPDATEs")
        self.firstname=firstname.lower()
        self.surname=surname.lower()
        self.email=email.lower()
        self.height=height
        self.address_line_1=address_line_1.lower()
        self.city=city.lower()
        self.postcode=postcode.upper()

    def update_password(self, new_password):
        """
        Updates the password.
        """
        self.password=bcrypt.generate_password_hash(new_password)

    def __repr__(self):
        """
        Depicts how the object is represented when printed out in the
        command line.
        """
        return '<Name {}'.format(self.firstname+self.surname)