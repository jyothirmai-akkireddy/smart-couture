from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from models.user import db, User, OTP
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

auth_bp = Blueprint('auth', __name__)


# ---------------------------------------------------
# SEND OTP EMAIL
# ---------------------------------------------------

def send_otp_email(email, otp_code):

    try:

        sender_email = os.environ.get('MAIL_USERNAME', '')
        sender_password = os.environ.get('MAIL_PASSWORD', '')

        if not sender_email or not sender_password:

            print("❌ Email credentials not configured")
            return False

        message = MIMEMultipart()

        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = 'StyleSense AI - Password Reset OTP'

        body = f"""
Hello,

Your OTP for password reset is: {otp_code}

This OTP expires in 10 minutes.

StyleSense AI Team
"""

        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender_email, sender_password)

        server.send_message(message)

        server.quit()

        print("✅ OTP sent")

        return True

    except Exception as e:

        print("❌ Email error:", e)

        return False


# ---------------------------------------------------
# SIGNUP
# ---------------------------------------------------

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':

        return render_template('signup.html')

    data = request.get_json() if request.is_json else request.form

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:

        return jsonify({'error': 'All fields required'}), 400

    if User.query.filter_by(email=email).first():

        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=username).first():

        return jsonify({'error': 'Username already exists'}), 400


    user = User(username=username, email=email)

    user.set_password(password)

    try:

        db.session.add(user)

        db.session.commit()

        session['user_id'] = user.id

        session['username'] = user.username

        return jsonify({

            'message': 'Signup successful',

            'redirect': url_for('dashboard.dashboard')

        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({'error': str(e)}), 500


# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')

    data = request.get_json() if request.is_json else request.form

    email = data.get('email')
    password = data.get('password')

    if not email or not password:

        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):

        return jsonify({'error': 'Invalid credentials'}), 401

    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({

        'message': 'Login successful',

        'redirect': url_for('dashboard.dashboard')

    }), 200


# ---------------------------------------------------
# LOGOUT
# ---------------------------------------------------

@auth_bp.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('index'))


# ---------------------------------------------------
# FORGOT PASSWORD
# ---------------------------------------------------

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'GET':

        return render_template('forgot_password.html')

    data = request.get_json() if request.is_json else request.form

    email = data.get('email')

    if not email:

        return jsonify({'error': 'Email required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:

        return jsonify({'error': 'User not found'}), 404

    otp_code = str(random.randint(100000, 999999))

    expires_at = datetime.utcnow() + timedelta(minutes=10)

    otp = OTP(

        email=email,

        otp_code=otp_code,

        expires_at=expires_at

    )

    db.session.add(otp)

    db.session.commit()

    if send_otp_email(email, otp_code):

        return jsonify({

            'message': 'OTP sent',

            'email': email

        })

    else:

        return jsonify({

            'error': 'Email service not configured'

        }), 500


# ---------------------------------------------------
# VERIFY OTP
# ---------------------------------------------------

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():

    data = request.get_json() if request.is_json else request.form

    email = data.get('email')

    otp_code = data.get('otp')

    otp = OTP.query.filter_by(

        email=email,

        otp_code=otp_code,

        used=False

    ).filter(

        OTP.expires_at > datetime.utcnow()

    ).first()

    if not otp:

        return jsonify({'error': 'Invalid OTP'}), 400

    otp.used = True

    db.session.commit()

    return jsonify({'message': 'OTP verified'})


# ---------------------------------------------------
# RESET PASSWORD
# ---------------------------------------------------

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():

    data = request.get_json() if request.is_json else request.form

    email = data.get('email')

    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:

        return jsonify({'error': 'User not found'}), 404

    user.set_password(password)

    db.session.commit()

    return jsonify({'message': 'Password reset successful'})
