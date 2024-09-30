import os
import requests
from flask import Flask, request, jsonify, render_template, Response
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COMPANY_INGREDIENTS = {
    "Nabisco": "Nabisco Wheat Thins",
    "Kraft": "Kraft Mayo",
    "Nestle": "Nestle Chocolate Chips"
}

@app.route('/')
def index():
    return render_template('index.html', companies=COMPANY_INGREDIENTS.keys())

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    company = data.get('company')
    ingredients = data.get('ingredients')
    options = data.get('options', {})

    # Ensure ingredients is a list
    if isinstance(ingredients, str):
        ingredients = [ingredient.strip() for ingredient in ingredients.split(',') if ingredient.strip()]

    if not company or company not in COMPANY_INGREDIENTS or not ingredients:
        logger.warning("Invalid input: Company or ingredients missing or invalid.")
        return jsonify({"error": "Invalid input. Please select a valid company and provide ingredients."}), 400

    logger.info(f"Received request: Company - {company}, Ingredients - {ingredients}")

    company_ingredient = COMPANY_INGREDIENTS[company]
    all_ingredients = ingredients + [company_ingredient]

    prompt_text = (
        f"Create a recipe using the following ingredients for {company}: {', '.join(all_ingredients)}. "
        f"Make sure to include {company_ingredient} as a key ingredient. Format the recipe as follows:\n\n"
        "Name: [Recipe Name]\n"
        "Tagline: [A short and catchy tagline]\n"
        "Ingredients:\n"
        "- [list each ingredient with quantity]\n"
        "Instructions:\n"
        "1. [Step-by-step cooking instructions]\n"
    )

    payload = {
        "model": "llama3",  # Update the model name to Llama 3
        "prompt": prompt_text,
        "options": options
    }

    logger.info(f"Sending payload to Ollama: {payload}")

    def generate():
        try:
            with requests.post('http://ollama:11434/api/generate', json=payload, stream=True, timeout=120) as response:
                response.raise_for_status()

                logger.info("Streaming Ollama response...")

                # Stream the response back to the client as it arrives
                for chunk in response.iter_content(chunk_size=128):
                    if chunk:
                        yield chunk.decode('utf-8')

        except requests.exceptions.Timeout:
            logger.error("Request to Ollama timed out.")
            yield json.dumps({"error": "Request to the recipe generator timed out. Please try again later."})
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Ollama failed: {e}")
            yield json.dumps({"error": "Failed to communicate with the recipe generator."})

    return Response(generate(), content_type='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
