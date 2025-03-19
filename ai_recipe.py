# # from llama_cpp import Llama
# #
# # # Initialize the model
# # llm = Llama(
# #     model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",  # Path to your model
# #     n_ctx=2048,  # Context window size
# #     n_threads=4,  # Use 4 CPU cores (adjust based on your machine)
# #     verbose=False  # Disable debug logs
# # )
# #
# #
# # def generate_recipe(ingredients, cuisine="any"):
# #     prompt = f"""Generate a detailed recipe using {ingredients} (cuisine: {cuisine}).
# #     Include ingredients, steps, and cooking time. Format the response clearly with headings."""
# #
# #     response = llm(
# #         prompt,
# #         max_tokens=200,  # Adjust based on desired recipe length
# #         temperature=0.7,  # Creativity (0=strict, 1=creative)
# #     )
# #
# #     return response["choices"][0]["text"]
#
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#
# def generate_recipe(ingredients, cuisine="any"):
#     prompt = f"Generate a {cuisine} recipe using {ingredients}..."
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt)
#     return response.text

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