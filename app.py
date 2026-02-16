from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from config import config
from models.user import db
import os

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.ai_routes import ai_bp
    from routes.profile_routes import profile_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(profile_bp)
    
    # Create upload folder
    os.makedirs('static/uploads', exist_ok=True)
    
    # Landing page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Create tables
    with app.app_context():
        db.create_all()
        seed_database()
    
    return app

def seed_database():
    """Seed database with sample products"""
    from models.user import Product
    
    # Check if products already exist
    if Product.query.count() > 0:
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
            'climate_match': 'warm'
        },
        {
            'name': 'Slim Fit Jeans',
            'brand': 'Levi\'s',
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
            'name': 'Casual Sneakers',
            'brand': 'Nike',
            'price': 4999,
            'rating': 4.8,
            'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
            'product_url': 'https://www.flipkart.com/search?q=sneakers',
            'category': 'shoes',
            'description': 'Comfortable everyday sneakers',
            'skin_tone_match': 'all',
            'climate_match': 'all'
        },
        {
            'name': 'Summer Dress',
            'brand': 'Zara',
            'price': 2999,
            'rating': 4.6,
            'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
            'product_url': 'https://www.ajio.com/search/?text=dress',
            'category': 'dress',
            'description': 'Light floral summer dress',
            'skin_tone_match': 'all',
            'climate_match': 'hot'
        },
        {
            'name': 'Leather Jacket',
            'brand': 'Zara',
            'price': 5999,
            'rating': 4.9,
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            'product_url': 'https://www.amazon.in/s?k=leather+jacket',
            'category': 'jacket',
            'description': 'Premium leather jacket',
            'skin_tone_match': 'all',
            'climate_match': 'cold'
        },
        {
            'name': 'Cotton Shirt',
            'brand': 'Peter England',
            'price': 1299,
            'rating': 4.4,
            'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400',
            'product_url': 'https://www.myntra.com/shirts',
            'category': 'shirt',
            'description': 'Formal cotton shirt',
            'skin_tone_match': 'all',
            'climate_match': 'cool'
        },
        {
            'name': 'Sports Shorts',
            'brand': 'Adidas',
            'price': 1499,
            'rating': 4.5,
            'image_url': 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400',
            'product_url': 'https://www.flipkart.com/search?q=sports+shorts',
            'category': 'pants',
            'description': 'Breathable sports shorts',
            'skin_tone_match': 'all',
            'climate_match': 'hot'
        },
        {
            'name': 'Hoodie',
            'brand': 'H&M',
            'price': 1999,
            'rating': 4.6,
            'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400',
            'product_url': 'https://www.ajio.com/search/?text=hoodie',
            'category': 'jacket',
            'description': 'Comfortable cotton hoodie',
            'skin_tone_match': 'all',
            'climate_match': 'cool'
        },
        {
            'name': 'Formal Blazer',
            'brand': 'Raymond',
            'price': 7999,
            'rating': 4.8,
            'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400',
            'product_url': 'https://www.myntra.com/blazers',
            'category': 'jacket',
            'description': 'Professional blazer for formal occasions',
            'skin_tone_match': 'all',
            'climate_match': 'cool'
        },
        {
            'name': 'Running Shoes',
            'brand': 'Puma',
            'price': 3999,
            'rating': 4.7,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
            'product_url': 'https://www.amazon.in/s?k=running+shoes',
            'category': 'shoes',
            'description': 'Lightweight running shoes',
            'skin_tone_match': 'all',
            'climate_match': 'all'
        },
        {
            'name': 'Polo T-Shirt',
            'brand': 'US Polo',
            'price': 1799,
            'rating': 4.5,
            'image_url': 'https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=400',
            'product_url': 'https://www.flipkart.com/search?q=polo+tshirt',
            'category': 'shirt',
            'description': 'Classic polo t-shirt',
            'skin_tone_match': 'all',
            'climate_match': 'warm'
        },
        {
            'name': 'Chino Pants',
            'brand': 'Allen Solly',
            'price': 2299,
            'rating': 4.6,
            'image_url': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400',
            'product_url': 'https://www.myntra.com/chinos',
            'category': 'pants',
            'description': 'Smart casual chinos',
            'skin_tone_match': 'all',
            'climate_match': 'warm'
        },
        {
            'name': 'Sunglasses',
            'brand': 'Ray-Ban',
            'price': 4999,
            'rating': 4.9,
            'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400',
            'product_url': 'https://www.amazon.in/s?k=sunglasses',
            'category': 'accessories',
            'description': 'UV protection sunglasses',
            'skin_tone_match': 'all',
            'climate_match': 'hot'
        },
        {
            'name': 'Backpack',
            'brand': 'Wildcraft',
            'price': 2499,
            'rating': 4.5,
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400',
            'product_url': 'https://www.flipkart.com/search?q=backpack',
            'category': 'accessories',
            'description': 'Durable travel backpack',
            'skin_tone_match': 'all',
            'climate_match': 'all'
        },
        {
            'name': 'Winter Coat',
            'brand': 'Jack & Jones',
            'price': 6999,
            'rating': 4.7,
            'image_url': 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400',
            'product_url': 'https://www.ajio.com/search/?text=coat',
            'category': 'jacket',
            'description': 'Warm winter coat',
            'skin_tone_match': 'all',
            'climate_match': 'cold'
        },
        {
            'name': 'Casual Watch',
            'brand': 'Fastrack',
            'price': 1999,
            'rating': 4.4,
            'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400',
            'product_url': 'https://www.myntra.com/watches',
            'category': 'accessories',
            'description': 'Stylish everyday watch',
            'skin_tone_match': 'all',
            'climate_match': 'all'
        },
        {
            'name': 'Ankle Boots',
            'brand': 'Clarks',
            'price': 5499,
            'rating': 4.8,
            'image_url': 'https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=400',
            'product_url': 'https://www.amazon.in/s?k=boots',
            'category': 'shoes',
            'description': 'Leather ankle boots',
            'skin_tone_match': 'all',
            'climate_match': 'cold'
        },
        {
            'name': 'Cardigan',
            'brand': 'Marks & Spencer',
            'price': 2799,
            'rating': 4.6,
            'image_url': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400',
            'product_url': 'https://www.myntra.com/cardigans',
            'category': 'jacket',
            'description': 'Cozy knit cardigan',
            'skin_tone_match': 'all',
            'climate_match': 'cool'
        },
        {
            'name': 'Formal Trousers',
            'brand': 'Van Heusen',
            'price': 1899,
            'rating': 4.5,
            'image_url': 'https://images.unsplash.com/photo-1594938291221-94f18cbb5660?w=400',
            'product_url': 'https://www.flipkart.com/search?q=formal+trousers',
            'category': 'pants',
            'description': 'Professional formal trousers',
            'skin_tone_match': 'all',
            'climate_match': 'all'
        },
        {
            'name': 'Canvas Bag',
            'brand': 'Lavie',
            'price': 1499,
            'rating': 4.3,
            'image_url': 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400',
            'product_url': 'https://www.ajio.com/search/?text=bag',
            'category': 'accessories',
            'description': 'Trendy canvas tote bag',
            'skin_tone_match': 'all',
            'climate_match': 'all'
        }
    ]
    
    for product_data in sample_products:
        product = Product(**product_data)
        db.session.add(product)
    
    try:
        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
