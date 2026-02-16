import requests
import os

class ClimateEngine:
    """Weather-based recommendation engine"""
    
    def __init__(self):
        self.api_key = os.environ.get('WEATHER_API_KEY', '')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city="London"):
        """Get current weather for a city"""
        if not self.api_key:
            # Return mock data if API key not available
            return {
                'temperature': 20,
                'condition': 'Clear',
                'description': 'clear sky'
            }
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': data['main']['temp'],
                    'condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity']
                }
            else:
                return self._get_mock_weather()
        
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather()
    
    def _get_mock_weather(self):
        """Return mock weather data"""
        return {
            'temperature': 22,
            'condition': 'Clear',
            'description': 'pleasant weather'
        }
    
    def get_climate_recommendation(self, weather_data):
        """Get clothing recommendations based on weather"""
        temp = weather_data.get('temperature', 20)
        condition = weather_data.get('condition', 'Clear')
        
        recommendations = {
            'climate_type': '',
            'suggestions': [],
            'avoid': []
        }
        
        # Temperature-based recommendations
        if temp < 10:
            recommendations['climate_type'] = 'cold'
            recommendations['suggestions'] = [
                'Heavy jackets and coats',
                'Sweaters and hoodies',
                'Long pants and jeans',
                'Boots',
                'Scarves and gloves'
            ]
            recommendations['avoid'] = ['Shorts', 'Tank tops', 'Sandals']
        
        elif 10 <= temp < 20:
            recommendations['climate_type'] = 'cool'
            recommendations['suggestions'] = [
                'Light jackets',
                'Long sleeve shirts',
                'Jeans or chinos',
                'Sneakers',
                'Layered outfits'
            ]
            recommendations['avoid'] = ['Heavy coats', 'Shorts']
        
        elif 20 <= temp < 28:
            recommendations['climate_type'] = 'warm'
            recommendations['suggestions'] = [
                'T-shirts and light tops',
                'Cotton clothing',
                'Light pants or jeans',
                'Sneakers or loafers',
                'Light layers'
            ]
            recommendations['avoid'] = ['Heavy jackets', 'Thick sweaters']
        
        else:  # temp >= 28
            recommendations['climate_type'] = 'hot'
            recommendations['suggestions'] = [
                'Cotton t-shirts',
                'Shorts',
                'Light breathable fabrics',
                'Sandals or light shoes',
                'Sunglasses and hats'
            ]
            recommendations['avoid'] = ['Jackets', 'Long sleeves', 'Heavy fabrics']
        
        # Condition-based additions
        if 'Rain' in condition or 'Drizzle' in condition:
            recommendations['suggestions'].append('Waterproof jacket or umbrella')
            recommendations['avoid'].append('Suede or non-waterproof materials')
        
        if 'Snow' in condition:
            recommendations['suggestions'].append('Winter boots and warm layers')
        
        return recommendations
    
    def get_recommended_climate_match(self, weather_data):
        """Get climate match string for product filtering"""
        temp = weather_data.get('temperature', 20)
        
        if temp < 10:
            return 'cold'
        elif 10 <= temp < 20:
            return 'cool'
        elif 20 <= temp < 28:
            return 'warm'
        else:
            return 'hot'
