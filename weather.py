from ai.climate_engine import ClimateEngine

def get_weather_recommendations(city="London"):
    """Get weather-based clothing recommendations"""
    engine = ClimateEngine()
    weather = engine.get_weather(city)
    recommendations = engine.get_climate_recommendation(weather)
    
    return {
        'weather': weather,
        'recommendations': recommendations,
        'climate_match': engine.get_recommended_climate_match(weather)
    }
