from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to call the Ollama API
def call_ollama_api(company, ingredients):
    try:
        ollama_api_url = "http://ollama-app:8000"  # Adjust URL if necessary
        payload = {
            "company": company,
            "ingredients": ingredients
        }
        response = requests.post(ollama_api_url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No text returned from Ollama")
    except requests.exceptions.RequestException as e:
        return f"Error with Ollama: {str(e)}"

# Function to call the Mistral API (mock or real API)
def call_mistral_api(company, ingredients):
    try:
        mistral_api_url = "http://mistral-app:8000"  # Replace with actual API URL
        payload = {
            "company": company,
            "ingredients": ingredients
        }
        response = requests.post(mistral_api_url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No text returned from Mistral")
    except requests.exceptions.RequestException as e:
        return f"Error with Mistral: {str(e)}"

# Function to call the LLaMA API (mock or real API)
def call_llama_api(company, ingredients):
    try:
        llama_api_url = "http://llama-app:8000"  # Replace with actual API URL
        payload = {
            "company": company,
            "ingredients": ingredients
        }
        response = requests.post(llama_api_url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No text returned from LLaMA")
    except requests.exceptions.RequestException as e:
        return f"Error with LLaMA: {str(e)}"

# POST route to get a recipe and query multiple LLMs
@app.route('/get-recipe', methods=['POST'])
def get_recipe():
    data = request.get_json()
    company = data.get("company")
    ingredients = data.get("ingredients")

    # Validate input
    if not company or not ingredients:
        return jsonify({"error": "Both 'company' and 'ingredients' are required"}), 400

    # Call multiple LLM APIs
    ollama_response = call_ollama_api(company, ingredients)
    mistral_response = call_mistral_api(company, ingredients)
    llama_response = call_llama_api(company, ingredients)

    # Aggregate results from all LLMs
    result = {
        "ollama": ollama_response,
        "mistral": mistral_response,
        "llama": llama_response
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
