import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ai_recipe import detect_ingredients_from_image, generate_recipe, send_recipe_email
import re
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        ingredients = detect_ingredients_from_image(image_file.read())

        if "error" in ingredients.lower():
            return jsonify({"error": ingredients}), 400
        elif not ingredients:
            return jsonify({"error": "Failed to detect ingredients"}), 400

        return jsonify({"ingredients": ingredients})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_recipe_route():
    try:
        data = request.get_json()
        ingredients = data.get("ingredients")
        cuisine = data.get("cuisine", "any")

        if not ingredients:
            return jsonify({"error": "Ingredients required!"}), 400

        recipe = generate_recipe(ingredients, cuisine)
        return jsonify({"recipe": recipe})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/share-email', methods=['POST'])
def share_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        email = data.get("email")
        recipe = data.get("recipe")

        if not email or not recipe:
            return jsonify({"error": "Email and recipe required"}), 400

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Invalid email format"}), 400

        success, message = send_recipe_email(email, recipe)

        if not success:
            return jsonify({"error": f"Email failed: {message}"}), 500

        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)