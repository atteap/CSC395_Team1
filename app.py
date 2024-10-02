import os
import requests
from flask import Flask, request, jsonify, render_template
import logging
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
COMPANY_INGREDIENTS = {
    "Nabisco": "Nabisco Wheat Thins",
    "Kraft": "Kraft Mayo",
    "Nestle": "Nestle Chocolate Chips"
}
OLLAMA_API_URL = 'http://ollama:11434/api/generate'

@app.route('/')
def index():
    return render_template('index.html', companies=COMPANY_INGREDIENTS.keys())

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    company = data.get('company')
    ingredients = data.get('ingredients')
    options = data.get('options', {})

    # Ensure company name matches exactly
    if company not in COMPANY_INGREDIENTS:
        return jsonify({"error": "Invalid company. Please select a valid company."}), 400

    # Validate and format ingredients
    ingredients = format_ingredients(ingredients)

    if not is_valid_input(company, ingredients):
        return jsonify({"error": "Invalid input. Please select a valid company and provide ingredients."}), 400

    logger.info(f"Received request: Company - {company}, Ingredients - {ingredients}")

    company_ingredient = COMPANY_INGREDIENTS[company]
    prompt_text = create_prompt_text(company, ingredients, company_ingredient, options)

    logger.info(f"Sending payload to Ollama: {prompt_text}")

    try:
        recipe_data = request_recipe(prompt_text)
        return jsonify(recipe_data), 200

    except requests.exceptions.Timeout:
        logger.error("Request to Ollama timed out.")
        return jsonify({"error": "Request to the recipe generator timed out. Please try again later."}), 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Ollama failed: {e}")
        return jsonify({"error": "Failed to communicate with the recipe generator."}), 500
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        return jsonify({"error": "Invalid response format from the recipe generator."}), 500

def format_ingredients(ingredients):
    """Ensure ingredients is a list and strip whitespace."""
    if isinstance(ingredients, str):
        return [ingredient.strip() for ingredient in ingredients.split(',') if ingredient.strip()]
    return ingredients

def is_valid_input(company, ingredients):
    """Check if the provided company and ingredients are valid."""
    return company and company in COMPANY_INGREDIENTS and ingredients

def create_prompt_text(company, ingredients, company_ingredient, options):
    """Generate the prompt text for the recipe generation."""
    all_ingredients = ingredients + [company_ingredient]
    return (
        f"Create a recipe using the following ingredients for {company}: {', '.join(all_ingredients)}. "
        f"Make sure to include {company_ingredient} as a key ingredient. Format the recipe as follows:\n\n"
        "[Recipe Name]\n"
        "Tagline: [A short and catchy tagline]\n"
        "Ingredients:\n"
        "- [list each ingredient with quantity]\n"
        "Instructions:\n"
        "1. [Step-by-step cooking instructions]\n"
    )

def request_recipe(prompt_text):
    """Send the request to the Ollama API and handle streaming response."""
    payload = {
        "model": "llama3",
        "prompt": prompt_text
    }

    logger.info(f"Sending request to Ollama API: {OLLAMA_API_URL}")

    with requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=None) as response:
        response.raise_for_status()
        logger.info("Ollama response received (streaming).")

        # Initialize buffer to collect the streamed response
        complete_response = ""
        recipe_found = False  # To stop after the first valid recipe

        for chunk in response.iter_lines():
            if chunk and not recipe_found:  # Stop once the first recipe is found
                try:
                    chunk_data = json.loads(chunk)
                    complete_response += chunk_data['response']

                    # Stop when the "done" flag is found
                    if chunk_data.get('done', False):
                        recipe_found = True  # Stop after the first recipe
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing chunk: {e}")
                    raise

        logger.info(f"Complete response: {complete_response}")

        # Process and return the parsed recipe response
        return parse_recipe_response(complete_response)

def parse_recipe_response(complete_response):
    """Extract name, tagline, ingredients, and instructions from the complete response."""
    # Initialize variables
    name = ""
    tagline = ""
    ingredients = []
    instructions = []

    # Split the complete response into lines
    lines = complete_response.strip().splitlines()

    # Flags to track current section
    in_ingredients = False
    in_instructions = False

    # Iterate through the lines to find each part of the recipe
    for line in lines:
        line = line.strip()  # Strip whitespace

        # Extract Recipe Name
        if line.startswith("**") and line.endswith("**") and not name:
            name = line[2:-2].strip()  # Remove the ** markers
            continue  # Move to next line

        # Extract Tagline
        if line.startswith("**Tagline:**") or line.startswith("Tagline:"):
            tagline = line.split("Tagline:")[1].strip().strip('"')
            continue  # Move to next line

        # Identify the start of the Ingredients section
        if line.startswith("**Ingredients:**") or line.startswith("Ingredients:"):
            in_ingredients = True
            continue  # Move to next line

        # Identify the start of the Instructions section
        if line.startswith("**Instructions:**") or line.startswith("Instructions:"):
            in_instructions = True
            in_ingredients = False  # Exit ingredients section
            continue  # Move to next line

        # Collect Ingredients
        if in_ingredients:
            if line.startswith("-") or line.startswith("*"):  # Check for ingredient lines
                ingredients.append(line[1:].strip())  # Collect ingredient, remove the hyphen

        # Collect Instructions
        if in_instructions and line and not line.startswith("**Instructions:**"):
            # Remove the number from the instruction and strip whitespace
            instruction_text = ' '.join(line.split('.')[1:]).strip() if '.' in line else line
            instructions.append(instruction_text)  # Collect instruction

        if in_instructions and line.startswith("**") and line.endswith("**"):
            break

    # Return structured data
    return {
        "name": name,
        "tagline": tagline,
        "ingredients": ingredients,
        "instructions": instructions
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
