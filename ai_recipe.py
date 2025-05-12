import google.generativeai as genai
from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
ses_client = boto3.client(
    'ses',
    region_name=os.getenv("AWS_REGION", "us-east-2"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


def detect_ingredients_from_image(image_bytes):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = """Analyze this image for edible ingredients. 
        Return ONLY a comma-separated list (e.g., "chicken, tomatoes, rice"). 
        Skip non-edible items and packaging."""

        response = model.generate_content({
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}}
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


def send_recipe_email(recipient, recipe_text):
    try:
        # Hardcode verified emails for testing
        allowed_recipients = {
            "eklavyadtu@gmail.com",
            "eklavyab3@gmail.com"
        }

        if recipient.lower() not in allowed_recipients:
            return False, "Recipient not verified"

        response = ses_client.send_email(
            Source=os.getenv("SENDER_EMAIL"),
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': 'Your AI-Generated Recipe'},
                'Body': {
                    'Text': {'Data': recipe_text},
                    'Html': {'Data': f"<pre>{recipe_text}</pre>"}
                }
            }
        )
        return True, response['MessageId']
    except ClientError as e:
        return False, e.response['Error']['Message']