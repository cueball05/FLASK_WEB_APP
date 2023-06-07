from . import db  # from the __init__.py file import db which is a SQLAlchemy object
from flask_login import UserMixin # handles user authentication and status when user is logged in
from sqlalchemy.sql import func

# Classes which define the table structure in SQLAlchemy
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Note.user_id in Note table is a foreign key of User.id table


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
