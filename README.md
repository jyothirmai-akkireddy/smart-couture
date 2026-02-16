Project Setup Instructions

This repository contains a Python project that requires some initial setup before running. Follow these steps carefully.

1. Clone the Repository
git clone <your-repo-url>
cd <repository-folder>

2. Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

3. Install Required Packages

Install all required Python packages specified in requirements.txt:

pip install -r requirements.txt

4. Create Missing __init__.py Files

Some Python modules/folders may not have __init__.py files. To ensure they are recognized as packages, create empty __init__.py files in the following directories:

ai/
instance/
models/
routes/
utils/


You can quickly create them using:

# Windows
type nul > ai\__init__.py
type nul > instance\__init__.py
type nul > models\__init__.py
type nul > routes\__init__.py
type nul > utils\__init__.py

# macOS/Linux
touch ai/__init__.py
touch instance/__init__.py
touch models/__init__.py
touch routes/__init__.py
touch utils/__init__.py

5. Environment Variables

Create a .env file if it doesn't exist and add any required environment variables, for example:

# Example .env file
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here


Make sure to never share your API keys publicly.

6. Running the Project

Once everything is set up:

# Activate the virtual environment if not already active
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run the application
python app.py

7. Notes

__pycache__/ is ignored; Python will generate it automatically.

The venv/ folder is not included in Git and should be created locally.

Ensure all packages in requirements.txt are installed.

If you face any issues, make sure you are using Python 3.10+.
