import os
import sqlite3
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
import re
from langchain.schema import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key from environment variable
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "your_actual_gemini_api_key")

# Initialize the model
model = ChatGoogleGenerativeAI(
    model="models/gemini-1.0-pro-latest",
    temperature=0.7,  # Controls randomness
    top_p=0.8  # Controls nucleus sampling
)

# Flask app initialization
app = Flask(__name__)

# Serve images from a directory (e.g., /static/)
@app.route('/static/<path:filename>')
def serve_image(filename):
    return send_from_directory('static', filename)

# Function to connect to the SQLite database
def connect_db():
    connection = sqlite3.connect('apparel.db')
    return connection

# Function to get apparel image from the database
def get_image_from_db(apparel_name):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT image_path FROM apparel WHERE name LIKE ?"
    cursor.execute(query, ('%' + apparel_name + '%',))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # Return the image path
    return None

# Function to interact with Gemini AI and return recommendations
def get_gemini_suggestions(context):
    response = model(context)
    return response.content  # Return the chatbot's response text

# Function to extract apparel name from the text
def extract_apparel_name(recommendation_text):
    match = re.search(r'\[\[([^\]]+)\]\]', recommendation_text)
    if match:
        return match.group(1).strip()
    return None

# Flask route to handle chatbot requests
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')

    # Context for the chatbot
    context = [HumanMessage(content=user_message)]

    # Get recommendation from Gemini AI
    recommendation_text = get_gemini_suggestions(context)
    suggested_apparel_name = extract_apparel_name(recommendation_text)

    # Fetch the corresponding image from the database
    image_url = None
    if suggested_apparel_name:
        image_path = get_image_from_db(suggested_apparel_name)
        if image_path:
            image_url = f"/static/{image_path.split('/')[-1]}"  # Assuming images are served from /static/

    # Return the chatbot response and image URL (if available)
    return jsonify({
        'text': recommendation_text,
        'image_url': image_url
    })

if __name__ == '__main__':
    app.run(debug=True)
