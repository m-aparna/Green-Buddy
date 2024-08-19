from . import db
from flask_login import UserMixin


# Class for storing Users in db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # establish relationship with notes
    notes = db.relationship('Note')


# NOTES
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(100))  # New field for the title
    plant_species = db.Column(db.String(200))  # New field for the description
    details = db.Column(db.Text)  # New field for the details
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
