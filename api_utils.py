# api_utils.py

import os
import requests
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Get your OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

# Set the headers for the API request
headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "http://localhost",
    "Content-Type": "application/json"
}

# Function to get explanation for a given topic
def get_explanation(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.text}"
    

import re

def clean_text_for_speech(text):
    # Keeps only letters, digits, space, and math symbols
    return re.sub(r"[^\w\s\+\-\*\/=]", "", text)

