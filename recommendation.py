from models.user import Product, Like, Purchase
import random

class RecommendationEngine:
    """Product recommendation engine"""
    
    def __init__(self, user_id=None):
        self.user_id = user_id
    
    def get_recommendations(self, filters=None, limit=10):
        """Get product recommendations based on filters"""
        query = Product.query
        
        if filters:
            if 'category' in filters:
                query = query.filter(Product.category.in_(filters['category']))
            
            if 'skin_tone' in filters and filters['skin_tone']:
                query = query.filter(
                    (Product.skin_tone_match == filters['skin_tone']) |
                    (Product.skin_tone_match == 'all')
                )
            
            if 'climate' in filters and filters['climate']:
                query = query.filter(
                    (Product.climate_match == filters['climate']) |
                    (Product.climate_match == 'all')
                )
            
            if 'max_price' in filters:
                query = query.filter(Product.price <= filters['max_price'])
            
            if 'min_rating' in filters:
                query = query.filter(Product.rating >= filters['min_rating'])
        
        # Order by rating and get results
        products = query.order_by(Product.rating.desc()).limit(limit).all()
        
        return [p.to_dict() for p in products]
    
    def get_personalized_recommendations(self, limit=10):
        """Get personalized recommendations based on user history"""
        if not self.user_id:
            return self.get_recommendations(limit=limit)
        
        # Get user's liked products
        liked_products = Like.query.filter_by(user_id=self.user_id).all()
        liked_categories = list(set([
            Product.query.get(like.product_id).category 
            for like in liked_products 
            if Product.query.get(like.product_id)
        ]))
        
        if liked_categories:
            # Recommend products from liked categories
            products = Product.query.filter(
                Product.category.in_(liked_categories)
            ).order_by(Product.rating.desc()).limit(limit).all()
        else:
            # Default recommendations
            products = Product.query.order_by(Product.rating.desc()).limit(limit).all()
        
        return [p.to_dict() for p in products]
    
    def get_trending_products(self, limit=20):
        """Get trending/popular products"""
        products = Product.query.order_by(
            Product.rating.desc(),
            Product.id.desc()
        ).limit(limit).all()
        
        return [p.to_dict() for p in products]
    
    def get_similar_products(self, product_id, limit=5):
        """Get similar products based on category"""
        product = Product.query.get(product_id)
        if not product:
            return []
        
        similar = Product.query.filter(
            Product.category == product.category,
            Product.id != product_id
        ).order_by(Product.rating.desc()).limit(limit).all()
        
        return [p.to_dict() for p in similar]
