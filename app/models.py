from . import db
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150))

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    dob = db.Column(db.Date)
    blood_type = db.Column(db.String(5))
    phone = db.Column(db.String(20))
    address1 = db.Column(db.String(200))
    address2 = db.Column(db.String(200))

    reset_otp = db.Column(db.String(6), nullable=True) 
    otp_expiry = db.Column(db.DateTime, nullable=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), default="Upcoming")  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("Doctor", backref="appointments", lazy=True)
    user = db.relationship("User", backref="appointments", lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    speciality = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    fee = db.Column(db.Integer, nullable=False, default=500)
