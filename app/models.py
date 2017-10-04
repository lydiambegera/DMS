# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create an Users table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    orders = db.relationship('Order', backref='users',
                                lazy='dynamic')
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Organization(db.Model):
    """
    Create an Organization table
    """

    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Organization: {}>'.format(self.name)

class Agent(db.Model):
    """
    Create the agent table
    """
    __tablename__='agents'
    id = db.Column(db.Integer, primary_key=True)
    agent_name=db.Column(db.String(100))
    phone_number=db.Column(db.String(100))

    def __repr__(self):
        return '<Agent: {}>'.format(self.name)

class Site(db.Model):
    """
    Create the sites table
    """

    __tablename__='sites'

    id = db.Column(db.Integer, primary_key=True)
    business_name=db.Column(db.String(100))
    site_location=db.Column(db.String(100))
    agent_name=db.Column(db.String(100))
    phone_number=db.Column(db.String(100))
    latitude=db.Column(db.String(50))
    longitude=db.Column(db.String(50))
    status=db.Column(db.String(20))
    business_type=db.Column(db.String(100))
    competing_products=db.Column(db.String(100))
    upload_sketch=db.Column(db.String(100))
    power_management=db.Column(db.String(100))
    time_spent=db.Column(db.String(20))
    no_of_users=db.Column(db.String(20))
    demographics=db.Column(db.String(20))
    internet_available=db.Column(db.String(20))
    internet_connection=db.Column(db.String(20))
    device_security=db.Column(db.String(20))
    wifi_coverage=db.Column(db.String(100))
    survey_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date=db.Column(db.DateTime)
    approved_backhaul= db.Column(db.Integer, db.ForeignKey('backhaul_providers.id'))
    comments=db.Column(db.String(400))
    orders = db.relationship('Order', backref='sites',
                                lazy='dynamic')

    def __repr__(self):
        return '<Site: {}>'.format(self.name)

class Backhaul(db.Model):
    """
    Create the backhaul providers table
    """
    __tablename__='backhaul_providers'
    id = db.Column(db.Integer, primary_key=True)
    backhaul_name=db.Column(db.String(100))
    contact_person=db.Column(db.String(100))
    phone_number=db.Column(db.String(100))
    sites = db.relationship('Site', backref='backhaul_providers',
                                lazy='dynamic')

    def __repr__(self):
        return '<Backhaul: {}>'.format(self.id)

class Order(db.Model):
    """
    Create the order table
    """

    __tablename__='orders'

    id = db.Column(db.Integer, primary_key=True)
    order_date=db.Column(db.DateTime)
    deployment_scheduled_date=db.Column(db.DateTime)
    deployment_date=db.Column(db.DateTime)
    deployed_by=db.Column(db.Integer, db.ForeignKey('users.id'))
    site_id=db.Column(db.Integer, db.ForeignKey('sites.id'))
    mac_address=db.Column(db.String(50))
    pre_deployment_date=db.Column(db.DateTime)
    tools_needed=db.Column(db.String(50))
    moja_wifi_access=db.Column(db.String(100))
    moja_content_access=db.Column(db.String(100))
    working_internet=db.Column(db.String(100))
    site_photo=db.Column(db.String(100))

    def __repr__(self):
        return '<Site: {}>'.format(self.name)
