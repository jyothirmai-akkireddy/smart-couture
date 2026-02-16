from flask import Blueprint, render_template, session, redirect, url_for
from models.user import Product, User
from ai.assistant import AIAssistant
from ai.climate_engine import ClimateEngine
from datetime import datetime
from functools import wraps


# ---------------------------------------------------
# CREATE BLUEPRINT
# ---------------------------------------------------

dashboard_bp = Blueprint('dashboard', __name__)


# ---------------------------------------------------
# INITIALIZE AI SYSTEMS
# ---------------------------------------------------

assistant = AIAssistant()
climate_engine = ClimateEngine()


# ---------------------------------------------------
# CUSTOM LOGIN REQUIRED (SESSION BASED)
# ---------------------------------------------------

def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'user_id' not in session:

            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return wrapper


# ---------------------------------------------------
# DASHBOARD ROUTE
# ---------------------------------------------------

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():

    """
    Dashboard Features:
    - Weather detection
    - AI outfit advice
    - Climate-based product filtering
    - Personalized greeting
    """

    # ---------------------------------------------------
    # GET USER FROM SESSION
    # ---------------------------------------------------

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)

    if not user:
        session.clear()
        return redirect(url_for('auth.login'))


    # ---------------------------------------------------
    # USER CONTEXT
    # ---------------------------------------------------

    user_location = getattr(user, "location", None) or "Pune"

    user_context = {
        "skin_tone": getattr(user, "skin_tone", None),
        "preferences": getattr(user, "preferences", None),
        "location": user_location
    }


    # ---------------------------------------------------
    # WEATHER DATA
    # ---------------------------------------------------

    weather_data = None
    climate_type = "all"
    temperature = None

    try:

        weather_data = climate_engine.get_weather(user_location)

        if weather_data:

            temperature = weather_data.get("temperature")

            climate_info = climate_engine.get_climate_recommendation(weather_data)

            climate_type = climate_info.get("climate_type", "all")

    except Exception as e:

        print("Weather error:", e)


    # ---------------------------------------------------
    # GREETING
    # ---------------------------------------------------

    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good morning"

    elif current_hour < 18:
        greeting = "Good afternoon"

    else:
        greeting = "Good evening"


    # ---------------------------------------------------
    # AI WEATHER ADVICE
    # ---------------------------------------------------

    try:

        ai_prompt = f"""
        User is in {user_location}.
        Current temperature is {temperature}°C.
        Climate is {climate_type}.
        Recommend what to wear today.
        """

        weather_response = assistant.chat(
            ai_prompt,
            user_context
        )

        weather_advice = weather_response.get("response", "No advice available.")

    except Exception as e:

        print("AI error:", e)

        weather_advice = "Unable to generate style advice."


    # ---------------------------------------------------
    # FILTER PRODUCTS
    # ---------------------------------------------------

    try:

        if climate_type == "hot":

            recommended_products = Product.query.filter(
                Product.climate_match.in_(["hot", "warm", "all"])
            ).limit(8).all()

        elif climate_type == "cold":

            recommended_products = Product.query.filter(
                Product.climate_match.in_(["cold", "cool", "all"])
            ).limit(8).all()

        elif climate_type == "cool":

            recommended_products = Product.query.filter(
                Product.climate_match.in_(["cool", "warm", "all"])
            ).limit(8).all()

        else:

            recommended_products = Product.query.limit(8).all()

    except Exception as e:

        print("Product error:", e)

        recommended_products = []


    # ---------------------------------------------------
    # RENDER DASHBOARD
    # ---------------------------------------------------

    return render_template(
        "dashboard.html",
        user=user,
        greeting=greeting,
        weather_advice=weather_advice,
        products=recommended_products,
        weather=weather_data,
        climate=climate_type,
        location=user_location,
        temperature=temperature
    )


# ---------------------------------------------------
# ALL PRODUCTS PAGE
# ---------------------------------------------------

@dashboard_bp.route('/products')
@login_required
def products():

    try:

        all_products = Product.query.all()

    except Exception as e:

        print("Products error:", e)

        all_products = []

    return render_template(
        "products.html",
        products=all_products
    )
@dashboard_bp.route('/purchases')
@login_required
def purchases():
    from models.user import Purchase, Product

    user_id = session.get('user_id')

    purchases = (
        db.session.query(Product)
        .join(Purchase, Purchase.product_id == Product.id)
        .filter(Purchase.user_id == user_id)
        .all()
    )

    return render_template("purchases.html", products=purchases)
