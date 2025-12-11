from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user
from .models import db, Appointment, Doctor
from flask_mail import Message
from . import mail
from datetime import datetime
import random
import time
from sqlalchemy import func
from urllib.parse import unquote


routes = Blueprint('routes', __name__)
doctors_bp = Blueprint('doctors_bp', __name__)


@routes.route('/')
def home():
  appointments = None
  doctors = Doctor.query.all()

  if current_user.is_authenticated:
    appointments = Appointment.query.filter_by(user_id=current_user.id)
  return render_template('home.html', doctors=doctors, appointments=appointments)


@routes.route('/book-doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)  # get the selected doctor

    if request.method == 'POST':
        date_str = request.form['date']
        time_str = request.form['time']
        phone_number = request.form['phone_number']

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()

        new_appointment = Appointment(
            user_id=current_user.id,
            doctor_id=doctor.id,  
            date=date_obj,
            time=time_obj,
            phone_number=phone_number
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash(f'Appointment with {doctor.name} scheduled successfully!', 'success')

        return redirect(url_for('routes.confirmation', appointment_id=new_appointment.id))


    return render_template('book.html', doctor=doctor)

@routes.route('/book-appointment')
@login_required
def book_appointment():
    specialities = db.session.query(Doctor.speciality).distinct().all()
    specialities = [s[0] for s in specialities]
    return render_template('book_appointment.html', specialities=specialities)

@routes.route('/book-appointment/<speciality>')
@login_required
def book_by_speciality(speciality):
    doctors = Doctor.query.filter_by(speciality=speciality).all()
    return render_template('doctors_by_speciality.html', doctors=doctors, speciality=speciality)

@routes.route('/confirmation')
@login_required
def confirmation():
    appointment_id = request.args.get('appointment_id')
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('confirmation.html', appointment=appointment)


@doctors_bp.route('/doctors')
def show_doctors():
    all_doctors = Doctor.query.all()
    print("Doctors in DB:", all_doctors)
    return render_template('doctors.html', doctors=all_doctors)

@doctors_bp.route('/speciality/<speciality>')
def doctors_by_speciality(speciality):
    decoded_speciality = unquote(speciality).replace('-', ' ').strip().lower()

    matched_speciality = (
        db.session.query(Doctor.speciality)
        .filter(func.lower(Doctor.speciality).like(f"%{decoded_speciality}%"))
        .first()
    )

    if matched_speciality:
        actual_speciality = matched_speciality[0]  
        filtered_doctors = Doctor.query.filter_by(speciality=actual_speciality).all()
        return render_template(
            'doctor_by_speciality.html',
            doctors=filtered_doctors,
            speciality=actual_speciality
        )
    else:
        flash("Sorry, no doctor is available for this speciality.", "warning")
        return redirect(url_for("doctors_bp.show_doctors")) 


@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/services')
def services():
    return render_template("services.html")

@routes.route('/faq')
def faq():
    return render_template("faq.html")

@routes.route('/contact')
def contact():
    return render_template("contact.html")

@routes.route('/profile')
@login_required
def profile():
    user = current_user

    if not (user.first_name and user.first_name.strip()) or not (user.phone and user.phone.strip()):
        return redirect(url_for('routes.edit_profile'))

    return render_template('profile.html', user=current_user)


@routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user

    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.address1 = request.form.get('address1')
        user.address2 = request.form.get('address2')
        user.gender = request.form.get('gender')
        user.blood_type = request.form.get('blood_type')
        user.phone = request.form.get('phone')

        dob_str = request.form.get('dob')
        if dob_str:  
            try:
                user.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format", "danger")

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('routes.profile'))

    return render_template("edit_profile.html", user=current_user)



@routes.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    now = datetime.now()
    return render_template(
        "appointments.html",
        appointments=appointments,
        current_date=now.date(),
        current_time=now.time()
    )

@routes.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        flash("You don't have permission to cancel this appointment.", "error")
        return redirect(url_for('main.appointments'))

    appointment.status = 'Cancelled'
    db.session.commit()
    flash("Appointment cancelled successfully.", "success")
    return redirect(url_for('routes.appointments'))


@doctors_bp.route('/seed-doctors')
def seed_doctors():
    from .models import db, Doctor

    doctors_list = [
    {
        "name": "Dr. Arjun Mehta",
        "speciality": "Cardiologist",
        "experience": 10,
        "description": "Expert in heart health, specializing in cardiovascular diagnostics, treatment plans, and long-term cardiac wellness strategies.",
        "image_url": "/static/images/male-doctor.jpg",
        "fee": 700
    },
    {
        "name": "Dr. Priya Sharma",
        "speciality": "Pediatrician",
        "experience": 8,
        "description": "Passionate about child health, offering nurturing care from infancy through adolescence with warmth and expertise.",
        "image_url": "/static/images/female-doctor2.jpg",
        "fee": 600
    },
    {
        "name": "Dr. Rakesh Gupta",
        "speciality": "General Physician",
        "experience": 9,
        "description": "Dedicated to holistic care, diagnosing and managing everyday health concerns with compassion and clinical precision.",
        "image_url": "/static/images/male-doctor2.avif",
        "fee": 650
    },
    {
        "name": "Dr. Anjali Verma",
        "speciality": "Dermatologist",
        "experience": 11,
        "description": "Skilled in treating skin, hair, and nail conditions, with a focus on aesthetic clarity and dermatological health.",
        "image_url": "/static/images/female-doctor3.jpg",
        "fee": 500
    },
    {
        "name": "Dr. Sameer Khan",
        "speciality": "Orthopedic Surgeon",
        "experience": 10,
        "description": "Restores mobility and strength through expert joint care, fracture management, and personalized recovery plans for active living.",
        "image_url": "/static/images/male-doctor3.jpg",
        "fee": 800
    },
    {
        "name": "Dr. Neha Patil",
        "speciality": "Gynecologist",
        "experience": 9,
        "description": "Provides comprehensive women’s health services, from routine exams to reproductive care and hormonal balance.",
        "image_url": "/static/images/female-doctor4.jpg",
        "fee": 700
    },
    {
        "name": "Dr. Vivek Nair",
        "speciality": "General Physician",
        "experience": 15,
        "description": "Your go-to for everyday health, preventive care, and personalized treatment plans that keep life running smoothly.",
        "image_url": "/static/images/male-doctor4.jpg",
        "fee": 550
    },
    {
        "name": "Dr. Kavita Reddy",
        "speciality": "ENT Specialist",
        "experience": 7,
        "description": "Treats ear, nose, and throat conditions, enhancing sensory health and breathing comfort with targeted therapies.",
        "image_url": "/static/images/female-doctor5.jpg",
        "fee": 600
    },
    {
        "name": "Dr. Suresh Iyer",
        "speciality": "Cardiologist",
        "experience": 18,
        "description": "Passionate about protecting hearts—offering advanced cardiac care, diagnostics, and long-term wellness strategies.",
        "image_url": "/static/images/male-doctor5.avif",
        "fee": 900
    },
    {
        "name": "Dr. Meera Das",
        "speciality": "Psychiatrist",
        "experience": 24,
        "description": "Supports mental wellness through thoughtful diagnosis, therapy, and medication management tailored to individual needs.",
        "image_url": "/static/images/female-doctor6.jpg",
        "fee": 650
    },
    {
        "name": "Dr. Rohit Kulkarni",
        "speciality": "Gynecologist",
        "experience": 10,
        "description": "Supports women’s health across all life stages—menstrual care, fertility, pregnancy, and hormonal balance.",
        "image_url": "/static/images/male-doctor6.avif",
        "fee": 700
    },
    {
        "name": "Dr. Sneha Chawla",
        "speciality": "Pulmonologist",
        "experience": 12,
        "description": "Specialist in lung and respiratory care, helping patients breathe easier with advanced diagnostics and compassionate support.",
        "image_url": "/static/images/female-doctor7.jpg",
        "fee": 600
    },
    {
        "name": "Dr. Abhinav Joshi",
        "speciality": "General Physician",
        "experience": 23,
        "description": "Trusted for everyday health, preventive care, and personalized treatment that keeps your body balanced and strong.",
        "image_url": "/static/images/male-doctor7.jpg",
        "fee": 550
    },
    {
        "name": "Dr. Ritu Malhotra",
        "speciality": "Ophthalmologist",
        "experience": 8,
        "description": "Protects and restores vision through expert eye care, from routine exams to advanced treatments for clarity and comfort.",
        "image_url": "/static/images/female-doctor8.jpg",
        "fee": 650
    },
    {
        "name": "Dr. Anant Deshmukh",
        "speciality": "ENT Specialist",
        "experience": 16,
        "description": "Enhances breathing, hearing, and voice clarity with targeted treatments for sinus, throat, and ear conditions.",
        "image_url": "/static/images/male-doctor8.jpg",
        "fee": 700
    },
    {
        "name": "Dr. Pooja Bansal",
        "speciality": "Psychiatrist",
        "experience": 5,
        "description": "Guides emotional resilience with compassionate therapy and tailored treatment for anxiety, mood disorders, and mental clarity.",
        "image_url": "/static/images/female-doctor9.jpg",
        "fee": 500
    },
    {
        "name": "Dr. Manish Agarwal",
        "speciality": "Dermatologist",
        "experience": 17,
        "description": "Guides emotional wellness with thoughtful therapy, medication, and support for anxiety, depression, and trauma.",
        "image_url": "/static/images/male-doctor9.webp",
        "fee": 800
    },
    {
        "name": "Dr. Alka Soni",
        "speciality": "Pediatrician",
        "experience": 8,
        "description": "KiGentle and attentive care for children, from routine checkups to developmental milestones and vaccinations.",
        "image_url": "/static/images/female-doctor10.jpg",
        "fee": 600
    },
    {
        "name": "Dr. Gaurav Saxena",
        "speciality": "Pulmonologist",
        "experience": 8,
        "description": "Delivers specialized lung care, helping patients manage asthma, COPD, and breathing disorders with precision and empathy.",
        "image_url": "/static/images/male-doctor10.webp",
        "fee": 600
    },
    {
        "name": "Dr. Shalini Kapoor",
        "speciality": "Gynecologist",
        "experience": 5,
        "description": "Empowers women’s health through expert care in fertility, pregnancy, and hormonal wellness across all life stages.",
        "image_url": "/static/images/female-doctor11.jpg",
        "fee": 850
    },
    {
        "name": "Dr. Anika Bose",
        "speciality": "Dentist",
        "experience": 17,
        "description": "Specialist in diagnosing and treating allergies and immune system disorders.",
        "image_url": "/static/images/female-doctor12.jpg",
        "fee": 500
    },
    {
        "name": "Dr. Rajesh Iyer",
        "speciality": "Dentist",
        "experience": 12,
        "description": "Expert in arthritis and autoimmune diseases, providing personalized treatment plans.",
        "image_url": "/static/images/male-doctor11.avif",
        "fee": 600
    },
    {
        "name": "Dr. Meenal Joshi",
        "speciality": "Orthopedic Surgeon",
        "experience": 10,
        "description": "Focused on blood disorders, anemia, and clotting conditions with compassionate care.",
        "image_url": "/static/images/female-doctor.jpg",
        "fee": 750
    },
    {
        "name": "Dr. Vikram Desai",
        "speciality": "Ophthalmologist",
        "experience": 8,
        "description": "Dedicated to diagnosing and managing sleep disorders for better overall health.",
        "image_url": "/static/images/male-doctor12.jpg",
        "fee": 650
    }
]

    for doc in doctors_list:
        if not Doctor.query.filter_by(name=doc["name"]).first():
            new_doc = Doctor(
                name=doc["name"],
                speciality=doc["speciality"],
                description=doc["description"],
                experience=doc["experience"],
                image_url=doc["image_url"]
            )
            db.session.add(new_doc)

    db.session.commit()
    return "Doctors seeded successfully!"


@doctors_bp.route('/reset-doctors')
def reset_doctors():
    from .models import db, Doctor

    # Delete all doctors
    Doctor.query.delete()
    db.session.commit()

    # Seed doctors (use your full doctors list here)
    doctors_list = [ 
        # all your doctor dicts here
    ]

    for doc in doctors_list:
        new_doc = Doctor(
            name=doc["name"],
            speciality=doc["speciality"],
            experience=doc["experience"],
            description=doc.get("description", ""),
            image_url=doc["image_url"]
        )
        db.session.add(new_doc)
    db.session.commit()
    return "Doctors reset and seeded successfully!"




@doctors_bp.route('/debug/specialities')
def debug_specialities():
    from sqlalchemy import distinct
    specialities = db.session.query(distinct(Doctor.speciality)).all()
    return "<br>".join([s[0] for s in specialities])