from ai.climate_engine import ClimateEngine
import os
from groq import Groq


class AIAssistant:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')

        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

        self.model = "llama-3.3-70b-versatile"

        # Initialize climate engine
        self.climate_engine = ClimateEngine()

    # ---------------------------------------------------
    # MAIN CHAT FUNCTION
    # ---------------------------------------------------

    def chat(self, user_message, user_context=None, conversation_history=None):
        """
        Main chat function for AI assistant
        """

        if not self.client:
            return {
                'response': "AI service is not configured. Please add GROQ_API_KEY.",
                'products': []
            }

        # Detect city
        city = self._detect_city(user_message, user_context)

        # Build system prompt
        system_prompt = self._build_system_prompt(user_context, city)

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        if conversation_history:
            messages.extend(conversation_history[-6:])

        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )

            ai_response = response.choices[0].message.content.strip()

            # ✅ FIXED: actually return detected products
            products = self._extract_products(ai_response, user_message)

            return {
                'response': ai_response,
                'products': products
            }

        except Exception as e:
            return {
                'response': f"I apologize, but I encountered an error: {str(e)}",
                'products': []
            }

    # ---------------------------------------------------
    # CITY DETECTION
    # ---------------------------------------------------

    def _detect_city(self, user_message, user_context=None):

        cities = [
            "pune", "hyderabad", "bangalore", "mumbai",
            "delhi", "chennai", "kolkata", "ahmedabad",
            "rajahmundry", "vizag", "visakhapatnam"
        ]

        message_lower = user_message.lower()

        for city in cities:
            if city in message_lower:
                return city.capitalize()

        if user_context and user_context.get("location"):
            return user_context.get("location")

        return "Pune"

    # ---------------------------------------------------
    # WEATHER CONTEXT
    # ---------------------------------------------------

    def _get_weather_context(self, city):

        try:
            weather = self.climate_engine.get_weather(city)

            if not weather:
                return ""

            temp = weather.get("temperature")
            desc = weather.get("description", "")

            climate = self.climate_engine.get_climate_recommendation(weather)
            climate_type = climate.get("climate_type", "")

            weather_context = f"""

CURRENT WEATHER IN {city}:
Temperature: {temp}°C
Condition: {desc}
Climate: {climate_type}

STYLING RULES BASED ON WEATHER:
"""

            if climate_type == "hot":
                weather_context += """
Recommend breathable fabrics like cotton and linen.
Avoid heavy fabrics.
Prefer light colours and loose fits.
"""

            elif climate_type == "warm":
                weather_context += """
Recommend light casual outfits.
Comfortable fabrics preferred.
"""

            elif climate_type == "cool":
                weather_context += """
Recommend layering.
Light jackets or long sleeves ideal.
"""

            elif climate_type == "cold":
                weather_context += """
Recommend sweaters, jackets, and warm clothing.
"""

            return weather_context

        except Exception:
            return ""

    # ---------------------------------------------------
    # SYSTEM PROMPT
    # ---------------------------------------------------

    def _build_system_prompt(self, user_context, city):

        base_prompt = f"""
You are StyleSense AI, an expert fashion stylist in India.

You MUST give styling advice AND suggest specific outfit categories.

When recommending outfits, clearly mention clothing types like:
lehenga, saree, kurti, blouse, dupatta, dress, shoes, jacket, pants etc.

Be natural, human-like, and conversational.
Always personalise advice.

If user asks about buying something, suggest items clearly.
"""

        if user_context:
            base_prompt += f"""

USER PROFILE:
Skin Tone: {user_context.get('skin_tone', 'Not specified')}
Preferences: {user_context.get('preferences', 'Not specified')}
Location: {user_context.get('location', 'Not specified')}
"""

        weather_context = self._get_weather_context(city)

        if weather_context:
            base_prompt += weather_context

        return base_prompt

    # ---------------------------------------------------
    # PRODUCT EXTRACTION
    # ---------------------------------------------------

    def _extract_products(self, ai_response, user_message):

        keywords = {
            'shirt': ['shirt', 't-shirt', 'top'],
            'pants': ['pants', 'jeans', 'trousers'],
            'dress': ['dress', 'gown'],
            'shoes': ['shoes', 'sneakers', 'heels'],
            'jacket': ['jacket', 'coat'],
            'lehenga': ['lehenga'],
            'saree': ['saree'],
            'kurti': ['kurti'],
            'dupatta': ['dupatta'],
            'blouse': ['blouse'],
            'salwar': ['salwar'],
            'anarkali': ['anarkali'],
        }

        detected = []

        combined = (ai_response + " " + user_message).lower()

        for category, terms in keywords.items():
            for term in terms:
                if term in combined:
                    detected.append(category)
                    break

        return list(set(detected))

    # ---------------------------------------------------
    # OUTFIT GENERATOR
    # ---------------------------------------------------

    def generate_outfit_recommendation(self, occasion, weather=None, user_preferences=None):

        prompt = f"Create outfit for {occasion}"

        if weather:
            prompt += f"\nWeather: {weather}"

        if user_preferences:
            prompt += f"\nPreferences: {user_preferences}"

        return self.chat(prompt)
