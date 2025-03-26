import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
from bs4 import BeautifulSoup

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-002")

# Initialize Flask app
app = Flask(__name__)

# College website URL
COLLEGE_URL = "https://arts.vidhyasagar.in/"

def format_response(response_text):
    """Format response with structured HTML."""
    return response_text.replace("**", "<b>").replace("*", "<li>")

def get_gemini_response(user_query):
    """Generate response using Gemini API with structured formatting."""
    try:
        response = model.generate_content(user_query)
        if response.text:
            return format_response(response.text.strip())
        else:
            return "I'm sorry, I couldn't find an answer."
    except Exception as e:
        return f"Error: {str(e)}"

def scrape_college_website():
    """Scrape the college website for the latest data."""
    try:
        response = requests.get(COLLEGE_URL, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text_content = " ".join([p.text for p in soup.find_all("p")])
            return text_content[:1000]  # Limit response size
        else:
            return None
    except Exception:
        return None
@app.route("/")
def chatbot():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    # First, try Gemini response
    ai_response = get_gemini_response(user_input)

    # If Gemini fails, attempt to scrape website
    if "Sorry" in ai_response or "I couldn't find" in ai_response:
        scraped_data = scrape_college_website()
        if scraped_data:
            return jsonify({"response": scraped_data})

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
