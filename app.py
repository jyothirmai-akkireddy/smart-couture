from flask import Flask, render_template
from config import config
from models.user import db, Product
import os


# ---------------------------------------------------
# CREATE FLASK APPLICATION
# ---------------------------------------------------

def create_app(config_name='development'):

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)


    # ---------------------------------------------------
    # REGISTER BLUEPRINTS
    # ---------------------------------------------------

    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.ai_routes import ai_bp
    from routes.profile_routes import profile_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(profile_bp)


    # ---------------------------------------------------
    # CREATE UPLOAD FOLDER
    # ---------------------------------------------------

    upload_folder = os.path.join("static", "uploads")

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)


    # ---------------------------------------------------
    # LANDING PAGE
    # ---------------------------------------------------

    @app.route('/')
    def index():
        return render_template('index.html')


    # ---------------------------------------------------
    # DATABASE INITIALIZATION
    # ---------------------------------------------------

    with app.app_context():
        db.create_all()
        seed_database()

    return app


# ---------------------------------------------------
# DATABASE SEED FUNCTION
# ---------------------------------------------------

def seed_database():

    try:

        if Product.query.first():
            print("Database already seeded.")
            return

        sample_products = [

            {
                'name': 'Classic White T-Shirt',
                'brand': 'H&M',
                'price': 499,
                'rating': 4.5,
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                'product_url': 'https://www.amazon.in/s?k=white+tshirt',
                'category': 'shirt',
                'description': 'Comfortable cotton t-shirt',
                'skin_tone_match': 'all',
                'climate_match': 'hot'
            },

            {
                'name': 'Slim Fit Jeans',
                'brand': "Levi's",
                'price': 2499,
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'product_url': 'https://www.myntra.com/jeans',
                'category': 'pants',
                'description': 'Classic blue denim jeans',
                'skin_tone_match': 'all',
                'climate_match': 'cool'
            },

            {
                'name': 'Summer Dress',
                'brand': 'Zara',
                'price': 2999,
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
                'product_url': 'https://www.ajio.com/search/?text=dress',
                'category': 'dress',
                'description': 'Light breathable summer dress',
                'skin_tone_match': 'all',
                'climate_match': 'hot'
            },

            {
                'name': 'Winter Jacket',
                'brand': 'Zara',
                'price': 5999,
                'rating': 4.9,
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
                'product_url': 'https://www.amazon.in/s?k=jacket',
                'category': 'jacket',
                'description': 'Warm winter jacket',
                'skin_tone_match': 'all',
                'climate_match': 'cold'
            },

            {
                'name': 'Running Shoes',
                'brand': 'Nike',
                'price': 3999,
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
                'product_url': 'https://www.flipkart.com/search?q=running+shoes',
                'category': 'shoes',
                'description': 'Comfortable running shoes',
                'skin_tone_match': 'all',
                'climate_match': 'all'
            }

        ]


        for product_data in sample_products:
            product = Product(**product_data)
            db.session.add(product)

        db.session.commit()

        print("Database seeded successfully!")

    except Exception as e:

        db.session.rollback()

        print("Database seed error:", e)


# ---------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------

if __name__ == "__main__":

    app = create_app()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
