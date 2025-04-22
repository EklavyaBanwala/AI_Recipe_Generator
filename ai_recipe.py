import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def detect_ingredients_from_image(image_bytes):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = """Analyze this image for edible ingredients. 
        Return ONLY a comma-separated list (e.g., "chicken, tomatoes, rice"). 
        Skip non-edible items and packaging."""

        response = model.generate_content({
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_bytes
                    }
                }
            ]
        })
        return response.text.strip()

    except Exception as e:
        return f"Image analysis error: {str(e)}"


def generate_recipe(ingredients, cuisine="any"):
    try:
        prompt = f"""Generate a detailed {cuisine} recipe using: {ingredients}.
        Format with headings for Ingredients and Steps. Avoid extra text."""

        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Recipe generation error: {str(e)}"
