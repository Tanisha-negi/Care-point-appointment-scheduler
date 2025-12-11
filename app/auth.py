from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import random
from datetime import datetime, timedelta
from .models import User
from . import db, mail
from flask_mail import Message, Mail

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])  
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("No account found with that email address.", "danger")
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('auth.login'))
        
        session['user'] = user.name

        login_user(user, remember=remember)

        flash("Login successful! Welcome back.", "success")
        return redirect(url_for('routes.home'))
            
    return render_template("login.html")

@auth.route('/logout')
def logout():
    logout_user()
    session.pop('user', None)
    flash('You’ve been logged out. Take care 💙', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'warning')
            return render_template("login.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("login.html")

        otp = str(random.randint(100000, 999999))

        session['signup_name'] = name
        session['signup_email'] = email
        session['signup_password'] = generate_password_hash(password, method='pbkdf2:sha256')
        session['signup_otp'] = otp
        session['otp_expiry'] = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

        msg = Message(
            subject="CarePoint Signup OTP",
            recipients=[email],
            body=f"Your OTP for CarePoint signup is: {otp}. It will expire in 5 minutes."
        )
        mail.send(msg)

        flash("OTP has been sent to your email. Please verify.", "info")
        return redirect(url_for('auth.verify_signup_otp'))

    return render_template("signup_otp_verify.html")

@auth.route('/verify-signup-otp', methods=['GET', 'POST'])
def verify_signup_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        otp = session.get('signup_otp')
        expiry = session.get('otp_expiry')

        if not otp or not expiry:
            flash("Session expired. Please signup again.", "danger")
            return redirect(url_for('auth.signup'))

        if datetime.utcnow() > datetime.fromisoformat(expiry):
            flash("OTP expired. Please signup again.", "danger")
            return redirect(url_for('auth.signup'))

        if entered_otp == otp:
            new_user = User(
                name=session['signup_name'],
                email=session['signup_email'],
                password=session['signup_password']
            )
            db.session.add(new_user)
            db.session.commit()

            session.pop('signup_name', None)
            session.pop('signup_email', None)
            session.pop('signup_password', None)
            session.pop('signup_otp', None)
            session.pop('otp_expiry', None)

            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Invalid OTP. Please try again.", "danger")

    return render_template("signup_otp_verify.html")



@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not registered", "error")
            return redirect(url_for('auth.forgot_password'))

        flash("OTP sent to your email", "success")
        return redirect(url_for('auth.verify_otp', email=email))

    return render_template('forgot_password.html')


@auth.route('/request-otp', methods=['GET', 'POST'])
def request_otp():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not registered!", "danger")
            return redirect(url_for("auth.request_otp"))

        session['email'] = email

        otp = str(random.randint(100000, 999999))
        session['otp'] = otp  
        user.reset_otp = otp
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()

        try:
            msg = Message(
                subject="Your OTP Code",
                recipients=[email],
                body=f"Your OTP is: {otp}"
            )
            mail.send(msg)
            flash("OTP has been sent to your email.", "info")
        except Exception as e:
            flash(f"Failed to send OTP: {str(e)}", "danger")

        return redirect(url_for("auth.verify_otp"))

    return render_template("verify_otp.html")


@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    email = session.get('email')
    if not email:
        flash("Please start the process first.", "danger")
        return redirect(url_for("auth.request_otp"))

    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if user and user.reset_otp == entered_otp and user.otp_expiry > datetime.utcnow():
            flash("OTP verified successfully!", "success")
            return redirect(url_for('auth.reset_password'))  
        else:
            flash("Invalid or expired OTP!", "danger")

    return render_template("verify_otp.html", email=email)

@auth.route('/resend-otp')
def resend_otp():
    email = session.get('email')
    if not email:
        flash("No email found. Please start the process again.", "danger")
        return redirect(url_for("auth.request_otp"))

    otp = str(random.randint(100000, 999999))
    session['otp'] = otp

    user = User.query.filter_by(email=email).first()
    if user:
        user.reset_otp = otp
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()

    try:
        msg = Message(
            subject="Your OTP Code",
            recipients=[email],
            body=f"Your new OTP is: {otp}"
        )
        mail.send(msg)
        flash("A new OTP has been sent to your email.", "info")
    except Exception as e:
        flash(f"Failed to send email: {str(e)}", "danger")

    return redirect(url_for("auth.verify_otp"))


@auth.route('/reset-password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            user.password = generate_password_hash(new_password)
            user.reset_otp = None
            user.otp_expiry = None
            db.session.commit()

            flash("Password reset successful! Please log in.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Passwords do not match!", "danger")

    return render_template("reset_password.html", email=email)



