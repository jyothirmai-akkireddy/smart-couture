from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.user import db, User, Product, Purchase
from ai.assistant import AIAssistant
from ai.memory import MemoryEngine
from ai.recommendation import RecommendationEngine
from utils.weather import get_weather_recommendations
from functools import wraps
import urllib.parse


ai_bp = Blueprint('ai', __name__)


# --------------------------------------------------
# LOGIN REQUIRED DECORATOR
# --------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function


# --------------------------------------------------
# ASSISTANT PAGE
# --------------------------------------------------

@ai_bp.route('/assistant')
@login_required
def assistant():

    user_id = session.get('user_id')

    user = User.query.get(user_id)

    return render_template(
        'assistant.html',
        user=user
    )


# --------------------------------------------------
# DETECT LOCATION FROM MESSAGE
# --------------------------------------------------

def detect_location_from_message(message, user):

    message_lower = message.lower()

    # simple city detection list (you can expand)
    cities = [
        "rajahmundry", "hyderabad", "delhi", "mumbai", "chennai",
        "bangalore", "pune", "kolkata", "vizag", "visakhapatnam"
    ]

    for city in cities:
        if city in message_lower:

            # SAVE to user profile
            user.location = city.title()
            db.session.commit()

            return city.title()

    # fallback to saved location
    if user.location:
        return user.location

    # final fallback
    return "Rajahmundry"


# --------------------------------------------------
# CHAT API
# --------------------------------------------------

@ai_bp.route('/api/chat', methods=['POST'])
@login_required
def chat():

    data = request.get_json()

    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Message required'}), 400


    # --------------------------------------------------
    # GET USER
    # --------------------------------------------------

    user_id = session.get('user_id')

    user = User.query.get(user_id)


    # --------------------------------------------------
    # DETECT LOCATION PROPERLY  ✅ FIX
    # --------------------------------------------------

    location = detect_location_from_message(message, user)


    # --------------------------------------------------
    # GET WEATHER
    # --------------------------------------------------

    weather_data = get_weather_recommendations(location)


    # --------------------------------------------------
    # LOAD MEMORY
    # --------------------------------------------------

    memory_engine = MemoryEngine(user_id)

    user_memories = memory_engine.get_all()


    # --------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------

    user_context = {

        'skin_tone': user.skin_tone,

        'preferences': user.preferences,

        'memories': user_memories,

        'location': location,

        'weather': weather_data.get("weather"),

        'climate': weather_data.get("climate_match")

    }


    # --------------------------------------------------
    # CONVERSATION MEMORY
    # --------------------------------------------------

    if 'conversation_history' not in session:
        session['conversation_history'] = []

    conversation_history = session['conversation_history']


    # --------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------

    assistant = AIAssistant()

    response = assistant.chat(

        message,

        user_context,

        conversation_history

    )


    # SAVE HISTORY

    conversation_history.append({
        "role": "user",
        "content": message
    })

    conversation_history.append({
        "role": "assistant",
        "content": response['response']
    })

    session['conversation_history'] = conversation_history[-12:]


    # --------------------------------------------------
    # PRODUCT RECOMMENDATION
    # --------------------------------------------------

    products = []

    custom_generated = False


    if response.get('products'):

        recommender = RecommendationEngine(user_id)


        for category in response['products']:

            filters = {

                'category': [category],

                'climate': weather_data.get("climate_match")

            }

            cat_products = recommender.get_recommendations(

                filters=filters,

                limit=2

            )

            if cat_products:
                products.extend(cat_products)


        # FALLBACK SEARCH LINKS

        if len(products) < 3:

            generated_products = _generate_search_cards(

                message,

                response['products']

            )

            products.extend(generated_products)

            custom_generated = True


    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    seen = set()

    unique_products = []

    for p in products:

        pid = p.get('id') or p.get('name')

        if pid not in seen:

            seen.add(pid)

            unique_products.append(p)


    # MARK CUSTOM PRODUCTS

    if custom_generated:

        for p in unique_products:

            if p.get('id') is None:

                p['is_custom'] = True


    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

    return jsonify({

        'response': response['response'],

        'weather': weather_data,

        'location': location,

        'products': unique_products[:6]

    })


# --------------------------------------------------
# SEARCH CARD GENERATOR
# --------------------------------------------------

def _generate_search_cards(user_message, categories):

    base_term = user_message.strip()

    if len(base_term) < 5:
        base_term = "fashion outfit"


    products = []

    stores = [

        {
            'name': 'Amazon',
            'url_tpl': 'https://www.amazon.in/s?k={q}',
            'brand': 'Amazon'
        },

        {
            'name': 'Myntra',
            'url_tpl': 'https://www.myntra.com/{q}',
            'brand': 'Myntra'
        },

        {
            'name': 'Ajio',
            'url_tpl': 'https://www.ajio.com/search/?text={q}',
            'brand': 'Ajio'
        },

        {
            'name': 'Flipkart',
            'url_tpl': 'https://www.flipkart.com/search?q={q}',
            'brand': 'Flipkart'
        }

    ]


    default_image = "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400"


    for i, category in enumerate(categories[:4]):

        store = stores[i % len(stores)]

        search_q = urllib.parse.quote(f"{base_term} {category}")

        url = store['url_tpl'].format(q=search_q)

        products.append({

            'id': None,

            'name': f"{category.title()} Recommendation",

            'brand': store['brand'],

            'price': 'Search Online',

            'rating': '★',

            'image_url': default_image,

            'product_url': url,

            'category': category,

            'is_search_link': True

        })


    return products


# --------------------------------------------------
# CLEAR CHAT
# --------------------------------------------------

@ai_bp.route('/api/clear-chat', methods=['POST'])
@login_required
def clear_chat():

    session['conversation_history'] = []

    return jsonify({

        'message': 'Chat cleared'

    })


# --------------------------------------------------
# WEATHER API
# --------------------------------------------------

@ai_bp.route('/api/weather-recommendation')
@login_required
def weather_recommendation():

    user_id = session.get('user_id')

    user = User.query.get(user_id)

    city = user.location or "Rajahmundry"

    weather_data = get_weather_recommendations(city)

    recommender = RecommendationEngine(user_id)

    products = recommender.get_recommendations(

        filters={

            'climate': weather_data['climate_match']

        },

        limit=8

    )


    return jsonify({

        'city': city,

        'weather': weather_data['weather'],

        'recommendations': weather_data['recommendations'],

        'products': products

    })
