from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from werkzeug.utils import secure_filename
from datetime import datetime
import os

# ✅ FIXED IMPORT (Product is inside user.py)
from models.user import db, User, Like, Purchase, Product
from utils.image_processing import ImageProcessor


# ================= BLUEPRINT =================
profile_bp = Blueprint('profile', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# ================= LOGIN REQUIRED =================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# ================= HELPER =================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ================= PROFILE PAGE =================
@profile_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(session.get('user_id'))
    return render_template('profile.html', user=user)


# ================= LIKED PAGE =================
@profile_bp.route('/liked')
@login_required
def liked():
    user_id = session.get('user_id')

    # ✅ SIMPLER & CLEANER QUERY (uses relationship)
    user = User.query.get(user_id)
    liked_products = [like.product for like in user.likes]

    return render_template('liked.html', products=liked_products)


# ================= UPDATE PROFILE =================
@profile_bp.route('/api/update-profile', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get(session.get('user_id'))

    data = request.get_json() if request.is_json else request.form

    user.username = data.get('username', user.username)
    user.preferences = data.get('preferences', user.preferences)

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ================= UPLOAD PHOTO =================
@profile_bp.route('/api/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    user = User.query.get(session.get('user_id'))

    if 'photo' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['photo']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filename = secure_filename(f"user_{user.id}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        processor = ImageProcessor()
        skin_tone = processor.detect_skin_tone(filepath)

        user.profile_image = f"/static/uploads/{filename}"
        user.skin_tone = skin_tone

        db.session.commit()

        return jsonify({
            'message': 'Photo uploaded successfully',
            'skin_tone': skin_tone,
            'image_url': user.profile_image
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ================= VIRTUAL TRY-ON =================
@profile_bp.route('/api/virtual-tryon', methods=['POST'])
@login_required
def virtual_tryon():
    user_id = session.get('user_id')

    if 'user_photo' not in request.files or 'clothing_photo' not in request.files:
        return jsonify({'error': 'Both photos required'}), 400

    try:
        temp_folder = os.path.join(UPLOAD_FOLDER, 'temp')
        os.makedirs(temp_folder, exist_ok=True)

        user_path = os.path.join(temp_folder, f"user_{user_id}_temp.jpg")
        clothing_path = os.path.join(temp_folder, f"clothing_{user_id}_temp.jpg")

        request.files['user_photo'].save(user_path)
        request.files['clothing_photo'].save(clothing_path)

        processor = ImageProcessor()
        result_image = processor.process_for_virtual_tryon(user_path, clothing_path)

        if result_image is None:
            return jsonify({'error': 'Processing failed'}), 500

        result_filename = f"tryon_{user_id}_{int(datetime.utcnow().timestamp())}.jpg"
        result_path = os.path.join(UPLOAD_FOLDER, result_filename)

        processor.save_processed_image(result_image, result_path)

        os.remove(user_path)
        os.remove(clothing_path)

        return jsonify({
            'message': 'Virtual try-on complete',
            'result_url': f"/static/uploads/{result_filename}"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ================= USER STATS =================
@profile_bp.route('/api/user-stats')
@login_required
def user_stats():
    user_id = session.get('user_id')

    return jsonify({
        'likes': Like.query.filter_by(user_id=user_id).count(),
        'purchases': Purchase.query.filter_by(user_id=user_id).count(),
        'conversations': '∞'
    })


# ================= CHANGE PASSWORD =================
@profile_bp.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    user = User.query.get(session.get('user_id'))
    data = request.get_json()

    if not user.check_password(data.get('current_password', '')):
        return jsonify({'error': 'Current password incorrect'}), 400

    if len(data.get('new_password', '')) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    user.set_password(data['new_password'])

    try:
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
