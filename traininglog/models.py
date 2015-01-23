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

class Member(db.Model):

    """
    Entity for the member's personal details.
    """
    __tablename__ = "Member"

    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.Enum('male', 'female', name='gender'))
    height = db.Column(db.Float,nullable=False)
    address_line_1 = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    join_date = db.Column(db.DateTime,nullable=False)
    last_login_date = db.Column(db.DateTime,nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def __init__(self, firstname, surname, email, password, gender, height, address_line_1, city, postcode, join_date, last_login_date, is_admin=0, is_active=1):
        
        """
        Constructor sets all the fields in the databased based on the parameters.
        """
        self.firstname=firstname
        self.surname=surname
        self.email=email
        # Hash the password
        self.password=bcrypt.generate_password_hash(password)
        self.gender=gender
        self.height=height
        self.address_line_1=address_line_1
        self.city=city
        self.postcode=postcode
        self.join_date=join_date
        self.last_login_date=last_login_date
        self.is_admin=is_admin
        self.is_active=is_active

    def is_authenticated(self):
        return True

    def is_active(self):
        return bool(self.is_active)

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_last_login_date(self,last_login_date):
        self.last_login_date=last_login_date

    def get_full_name(self):
        return self.firstname.title() + " " + self.surname.title()

    def __repr__(self):
        return '<Name {}'.format(self.firstname+self.surname)