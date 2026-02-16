from models.user import db, Memory

class MemoryEngine:
    """AI Memory system for storing and retrieving user preferences"""
    
    def __init__(self, user_id):
        self.user_id = user_id
    
    def store(self, key, value):
        """Store a memory for the user"""
        try:
            # Check if memory already exists
            memory = Memory.query.filter_by(user_id=self.user_id, key=key).first()
            
            if memory:
                memory.value = str(value)
            else:
                memory = Memory(user_id=self.user_id, key=key, value=str(value))
                db.session.add(memory)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error storing memory: {e}")
            return False
    
    def retrieve(self, key):
        """Retrieve a specific memory"""
        memory = Memory.query.filter_by(user_id=self.user_id, key=key).first()
        return memory.value if memory else None
    
    def get_all(self):
        """Get all memories for the user"""
        memories = Memory.query.filter_by(user_id=self.user_id).all()
        return {m.key: m.value for m in memories}
    
    def delete(self, key):
        """Delete a specific memory"""
        try:
            Memory.query.filter_by(user_id=self.user_id, key=key).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting memory: {e}")
            return False
    
    def get_preferences_summary(self):
        """Get a summary of user preferences for AI context"""
        memories = self.get_all()
        
        summary = {
            'favorite_colors': memories.get('favorite_colors', 'Not specified'),
            'favorite_brands': memories.get('favorite_brands', 'Not specified'),
            'style_preference': memories.get('style_preference', 'Not specified'),
            'budget_range': memories.get('budget_range', 'Not specified'),
            'occasions': memories.get('frequent_occasions', 'Not specified')
        }
        
        return summary
    
    def learn_from_interaction(self, interaction_data):
        """Learn from user interactions and update memories"""
        if 'liked_category' in interaction_data:
            self.store('preferred_categories', interaction_data['liked_category'])
        
        if 'style_mentioned' in interaction_data:
            self.store('style_preference', interaction_data['style_mentioned'])
        
        if 'budget_mentioned' in interaction_data:
            self.store('budget_range', interaction_data['budget_mentioned'])
