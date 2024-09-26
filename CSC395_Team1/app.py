import os
import requests
from flask import Flask, request, jsonify, render_template
import logging
import json

app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of companies and their specific ingredients
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

    # Validate input
    if not company or company not in COMPANY_INGREDIENTS or not ingredients:
        logger.warning("Invalid input: Company or ingredients missing or invalid.")
        return jsonify({"error": "Invalid input. Please select a valid company and provide ingredients."}), 400

    logger.info(f"Received request: Company - {company}, Ingredients - {ingredients}")

    # Add company-specific ingredient to the prompt
    company_ingredient = COMPANY_INGREDIENTS[company]
    all_ingredients = ingredients + [company_ingredient]

    # Prepare structured prompt for Ollama API request
    prompt_text = (
        f"Create a recipe using the following ingredients for {company}: {', '.join(ingredients)}. "
        f"Make sure to include {company_ingredient} as a key ingredient. Format the recipe as follows:\n\n"
        "Name: [Recipe Name]\n"
        "Tagline: [A short and catchy tagline]\n"
        "Ingredients:\n"
        "- [list each ingredient with quantity]\n"
        "Instructions:\n"
        "1. [Step-by-step cooking instructions]\n"
    )

    payload = {
        "model": "orca-mini:3b-q4_1",
        "prompt": prompt_text,
        "options": options  # Include additional parameters if provided
    }

    logger.info(f"Sending payload to Ollama: {payload}")

    try:
        response = requests.post(f"{"http://ollama:11434"}/api/generate", json=payload, stream=True)
        response.raise_for_status()

        # Collect response lines
        recipe_data = []
        for line in response.iter_lines():
            if line:
                recipe_data.append(line)

        # Assuming the last line contains the final response
        final_response = recipe_data[-1].decode('utf-8')
        recipe_json = json.loads(final_response)  # Adjust based on actual response format

        logger.info(f"Ollama response received: {recipe_json}")

        # Parse the expected format from the response
        recipe_text = recipe_json.get("text", "")
        name = extract_section(recipe_text, "Name:")
        tagline = extract_section(recipe_text, "Tagline:")
        ingredients_list = extract_section(recipe_text, "Ingredients:")
        instructions = extract_section(recipe_text, "Instructions:")

        return jsonify({
            "name": name.strip() if name else "Unnamed Recipe",
            "tagline": tagline.strip() if tagline else "",
            "ingredients": ingredients_list.strip() if ingredients_list else [],
            "instructions": instructions.strip() if instructions else ""
        }), 200

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}, Response: {response.text if 'response' in locals() else 'No response'}")
        return jsonify({"error": "Failed to communicate with the recipe generator."}), 502
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request to Ollama failed: {req_err}")
        return jsonify({"error": "Failed to communicate with the recipe generator."}), 500
    except json.JSONDecodeError as json_err:
        logger.error(f"JSON decode error: {json_err}, Response: {response.text if 'response' in locals() else 'No response'}")
        return jsonify({"error": "Received invalid response from the recipe generator."}), 500
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        return jsonify({"error": "An unexpected error occurred."}), 500

def extract_section(text, section):
    """
    Extracts the text following the section header until the next header or end of text.
    """
    try:
        start_index = text.index(section) + len(section)
        end_index = text.find("\n", start_index)
        return text[start_index:end_index].strip()
    except ValueError:
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
