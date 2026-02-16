# StyleSense AI - Production-Grade AI Fashion Intelligence Platform

## 🌟 Overview

StyleSense AI is a fully functional, production-ready AI fashion styling web application with real shopping integration. It features a ChatGPT-like AI assistant, personalized recommendations, skin tone detection, weather-based suggestions, and direct shopping links to Amazon, Myntra, Ajio, Flipkart, and H&M.

## ✨ Features

### Core Features
- **AI Fashion Assistant**: ChatGPT-like conversational AI stylist powered by Groq (Llama 3.3 70B)
- **Infinite Product Carousel**: Auto-scrolling product showcase
- **Real Shopping Integration**: Direct buy links to top e-commerce platforms
- **Skin Tone Detection**: AI-powered skin tone analysis using OpenCV
- **Weather-Based Recommendations**: Climate-appropriate outfit suggestions
- **Memory System**: AI remembers user preferences and style choices
- **Virtual Try-On**: Basic image overlay try-on feature
- **User Authentication**: Complete signup/login/logout with JWT
- **Password Recovery**: OTP-based password reset via email

### User Features
- Personal profile with skin tone detection
- Liked products collection
- Purchase history tracking
- Personalized recommendations
- Real-time AI chat interface

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone/Extract the project**
```bash
cd stylesense_ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
```
http://localhost:5000
```

## 🔑 API Keys Required

### Essential (for full functionality):
- **GROQ_API_KEY**: Get free API key from https://console.groq.com
  - Used for AI assistant (Llama 3.3 70B)
  - Free tier: 30 requests/minute

### Optional:
- **WEATHER_API_KEY**: Get from https://openweathermap.org/api
  - Used for weather-based recommendations
  - App works without it (uses mock data)

- **Email Configuration**: For OTP password reset
  - MAIL_USERNAME and MAIL_PASSWORD
  - App works without it (OTP shown in console)

## 📁 Project Structure

```
stylesense_ai/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── models/
│   └── user.py          # Database models
├── routes/
│   ├── auth_routes.py   # Authentication endpoints
│   ├── dashboard_routes.py  # Dashboard endpoints
│   ├── ai_routes.py     # AI assistant endpoints
│   └── profile_routes.py    # Profile endpoints
├── ai/
│   ├── assistant.py     # AI assistant engine
│   ├── memory.py       # Memory system
│   ├── recommendation.py # Recommendation engine
│   └── climate_engine.py # Weather recommendations
├── utils/
│   ├── image_processing.py # Skin tone detection
│   └── weather.py       # Weather utilities
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html       # Landing page
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── assistant.html   # AI chat interface
│   ├── profile.html
│   ├── liked.html
│   ├── purchases.html
│   └── forgot_password.html
└── static/
    ├── css/
    ├── js/
    └── uploads/         # User uploaded images
```

## 🎨 Tech Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM
- **SQLite/PostgreSQL**: Database
- **Groq API**: AI model (Llama 3.3 70B)
- **OpenCV**: Image processing
- **bcrypt**: Password hashing

### Frontend
- **TailwindCSS**: Styling
- **Vanilla JavaScript**: Interactivity
- **Jinja2**: Templating

### AI/ML
- **Groq (Llama 3.3 70B)**: Conversational AI
- **OpenCV**: Skin tone detection
- **Custom recommendation engine**

## 🌐 Deployment

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Deployment Platforms

#### Render
1. Create new Web Service
2. Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add environment variables

#### Railway
1. New Project → Deploy from GitHub
2. Add environment variables
3. Railway auto-detects Flask app

#### Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile
git push heroku main
```

## 📝 Usage Guide

### 1. Sign Up
- Create account with username, email, password
- Automatic login after signup

### 2. Dashboard
- View trending products
- Infinite auto-scrolling carousel
- Like products
- Direct shopping links

### 3. AI Assistant
- Chat with AI stylist
- Get personalized recommendations
- Ask about outfits, occasions, style
- Receive product suggestions

### 4. Profile
- Upload photo for skin tone detection
- Update preferences
- View detected skin tone

### 5. Shopping
- Click "Buy Now" on any product
- Opens official e-commerce site
- Purchase tracked in history

## 🔒 Security Features

- Password hashing with bcrypt
- JWT session management
- Protected routes
- SQL injection prevention (SQLAlchemy ORM)
- CSRF protection
- Secure file uploads
- Environment variable configuration

## 📊 Database Schema

### Users
- id, username, email, password_hash
- skin_tone, profile_image, preferences
- created_at

### Products
- id, name, brand, price, rating
- image_url, product_url
- category, description
- skin_tone_match, climate_match

### Memories
- id, user_id, key, value
- created_at

### Likes
- id, user_id, product_id

### Purchases
- id, user_id, product_id, purchase_date

### OTPs
- id, email, otp_code, expires_at

## 🎯 Key Features Explained

### AI Assistant
- Uses Groq's Llama 3.3 70B model
- Conversational memory (last 10 messages)
- Context-aware responses
- Product recommendation integration

### Recommendation Engine
- Personalized based on user history
- Category-based filtering
- Skin tone matching
- Climate-appropriate suggestions

### Memory System
- Stores user preferences
- Learning from interactions
- Persistent across sessions

### Skin Tone Detection
- OpenCV-based HSV color analysis
- 5 categories: fair, light, medium, tan, deep
- Used for product matching

### Weather Integration
- Real-time weather API
- Temperature-based recommendations
- Condition-aware suggestions

## 🐛 Troubleshooting

### Database not found
```bash
# Database auto-creates on first run
python app.py
```

### Missing API key
- Check .env file
- Ensure GROQ_API_KEY is set
- App works with limited features without optional keys

### Port already in use
```bash
# Change port in app.py or use:
python app.py --port 5001
```

### OpenCV installation issues
```bash
# On Linux:
pip install opencv-python-headless

# On Windows:
pip install opencv-python
```

## 📦 Sample Products

The app comes pre-seeded with 20 sample products from various categories:
- Shirts & T-shirts
- Pants & Jeans
- Shoes & Sneakers
- Jackets & Coats
- Dresses
- Accessories

All products link to real shopping platforms.

## 🔄 Updates & Maintenance

### Adding Products
Edit `seed_database()` in `app.py` or add via database

### Customizing AI
Edit prompts in `ai/assistant.py`

### Changing Styles
Modify TailwindCSS classes in templates

## 📄 License

This is a demo/educational project. Feel free to use and modify.

## 🤝 Support

For issues or questions:
- Check troubleshooting section
- Review code comments
- Test with sample data

## 🎉 Credits

- **AI Model**: Groq (Llama 3.3 70B)
- **UI Inspiration**: Modern SaaS products
- **Product Images**: Unsplash
- **Icons**: Heroicons

---

**Built with ❤️ for StyleSense AI**
