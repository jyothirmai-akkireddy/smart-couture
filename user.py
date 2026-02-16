from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ==========================================================
# USER MODEL
# ==========================================================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    skin_tone = db.Column(db.String(50))

    profile_image = db.Column(db.String(255))

    preferences = db.Column(db.Text)

    # ✅ ADD THIS LINE (CRITICAL FIX)
    location = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    # Relationships
    memories = db.relationship(
        'Memory',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    likes = db.relationship(
        'Like',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    purchases = db.relationship(
        'Purchase',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )


    # Password methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'skin_tone': self.skin_tone,
            'profile_image': self.profile_image,
            'preferences': self.preferences,
            'location': self.location,  # ✅ included
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ==========================================================
# PRODUCT MODEL
# ==========================================================

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    brand = db.Column(db.String(100))

    price = db.Column(db.Float)

    rating = db.Column(db.Float)

    image_url = db.Column(db.String(500))

    product_url = db.Column(db.String(500))

    category = db.Column(db.String(100))

    description = db.Column(db.Text)

    skin_tone_match = db.Column(db.String(50))

    climate_match = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    likes = db.relationship(
        'Like',
        backref='product',
        lazy=True,
        cascade='all, delete-orphan'
    )

    purchases = db.relationship(
        'Purchase',
        backref='product',
        lazy=True,
        cascade='all, delete-orphan'
    )


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'rating': self.rating,
            'image_url': self.image_url,
            'product_url': self.product_url,
            'category': self.category,
            'description': self.description,
            'skin_tone_match': self.skin_tone_match,
            'climate_match': self.climate_match
        }


# ==========================================================
# MEMORY MODEL
# ==========================================================

class Memory(db.Model):
    __tablename__ = 'memories'
    
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    key = db.Column(db.String(100), nullable=False)

    value = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ==========================================================
# LIKE MODEL
# ==========================================================

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================================
# PURCHASE MODEL
# ==========================================================

class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    purchase_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==========================================================
# OTP MODEL
# ==========================================================

class OTP(db.Model):
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), nullable=False)

    otp_code = db.Column(db.String(6), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    expires_at = db.Column(db.DateTime, nullable=False)

    used = db.Column(db.Boolean, default=False)
