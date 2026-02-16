# 🚀 QUICK START GUIDE

## Get Started in 3 Minutes!

### Step 1: Extract & Navigate
```bash
unzip stylesense_ai.zip
cd stylesense_ai
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Get Your Free Groq API Key (30 seconds)
1. Visit: https://console.groq.com
2. Sign up (free)
3. Go to API Keys
4. Create new key
5. Copy the key

### Step 4: Configure
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key:
GROQ_API_KEY=your-key-here
SECRET_KEY=any-random-string-here
```

### Step 5: Run!
```bash
python app.py
```

### Step 6: Open Browser
```
http://localhost:5000
```

## First Time Setup

1. **Sign Up**: Create an account
2. **Explore Dashboard**: See trending products
3. **Chat with AI**: Click "AI Assistant" in nav
4. **Upload Photo**: Go to Profile → Upload photo for skin tone detection
5. **Shop**: Click "Buy Now" on any product

## Test Accounts (Optional)

You can create your own accounts or use these test credentials if you set them up:
- Email: test@stylesense.com
- Password: Test123!

## Quick Commands

```bash
# Run development server
python app.py

# Run with custom port
python app.py  # Then edit app.py, change port

# Install in virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Minimum Requirements

✅ **Required:**
- Python 3.11+
- Groq API Key (free at console.groq.com)

❌ **NOT Required:**
- Weather API Key (uses mock data)
- Email credentials (shows OTP in console)
- GPU or special hardware

## Features You Can Try Immediately

1. **AI Stylist Chat**
   - "I need an outfit for a job interview"
   - "What should I wear in hot weather?"
   - "Recommend casual summer clothes"

2. **Product Shopping**
   - Browse infinite carousel
   - Like products
   - Get real shopping links

3. **Skin Tone Detection**
   - Upload your photo
   - Get AI skin tone analysis
   - Receive personalized matches

## Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"Port 5000 already in use"**
- Edit app.py, change last line to: `app.run(debug=True, port=5001)`

**"GROQ_API_KEY not found"**
- Make sure .env file exists
- Check GROQ_API_KEY is set in .env

**Database errors**
- Delete stylesense.db if it exists
- Restart app (auto-creates database)

## Need Help?

1. Read README.md for full documentation
2. Check .env.example for all configuration options
3. All features work locally without deployment

## Next Steps

- Deploy to Render/Railway (see README.md)
- Customize products in app.py
- Add your own API keys for full features
- Modify UI in templates/

---

**Enjoy building with StyleSense AI! 🎨✨**
