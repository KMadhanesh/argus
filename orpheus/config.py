# argus/orpheus/config.py

import os
from dotenv import load_dotenv

# Loads variables from a .env file
load_dotenv() 

# API Key for Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Other future configurations
# HERMES_API_URL = "http://localhost:5000"
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")