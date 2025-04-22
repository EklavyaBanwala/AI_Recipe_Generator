from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ai_recipe import detect_ingredients_from_image, generate_recipe
import time

app = Flask(__name__)
CORS(app)  # Enable CORS to avoid frontend-backend conflicts
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limit image uploads to 5MB

# Homepage: Serve the HTML template
@app.route('/')
def home():
    return render_template("index.html")

# Handle image uploads and ingredient detection
@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Detect ingredients from image
        ingredients = detect_ingredients_from_image(image_file.read())

        # Validate ingredients
        if "no ingredients detected" in ingredients.lower():
            return jsonify({"error": "No ingredients detected in the image."}), 400
        elif not ingredients:
            return jsonify({"error": "Failed to detect ingredients."}), 400

        return jsonify({"ingredients": ingredients})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generate recipe from ingredients (text or image)
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

if __name__ == '__main__':
    app.run(debug=True)
