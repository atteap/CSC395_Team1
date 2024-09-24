from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def call_ollama_api(company, ingredients):
    try:
        ollama_api_url = "http://ollama-app:8000/submit"
        payload = {
            "company": company,
            "ingredients": ingredients
        }
        response = requests.post(ollama_api_url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No text returned from Ollama")
    except requests.exceptions.RequestException as e:
        return f"Error with Ollama: {str(e)}"

def call_mistral_api(company, ingredients):
    try:
        mistral_api_url = "http://mistral-app:8000/submit"
        payload = {
            "company": company,
            "ingredients": ingredients
        }
        response = requests.post(mistral_api_url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No text returned from Mistral")
    except requests.exceptions.RequestException as e:
        return f"Error with Mistral: {str(e)}"

def call_llama_api(company, ingredients):
    try:
        llama_api_url = "http://llama-app:8000/submit"
        payload = {
            "company": company,
            "ingredients": ingredients
        }
        response = requests.post(llama_api_url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No text returned from LLaMA")
    except requests.exceptions.RequestException as e:
        return f"Error with LLaMA: {str(e)}"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    company = data.get("company")
    ingredients = data.get("ingredients")

    if not company or not ingredients:
        return jsonify({"error": "Both 'company' and 'ingredients' are required"}), 400

    ollama_response = call_ollama_api(company, ingredients)
    mistral_response = call_mistral_api(company, ingredients)
    llama_response = call_llama_api(company, ingredients)

    result = {
        "ollama": ollama_response,
        "mistral": mistral_response,
        "llama": llama_response
    }

    return jsonify(result), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Flask app is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
