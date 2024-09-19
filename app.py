from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-recipe', methods=['POST'])
def get_recipe():
    data = request.get_json()
    company = data.get("company")
    ingredients = data.get("ingredients")
    
    ollama_api_url = "http://ollama-app:8000"
    payload = {
        "company": company,
        "ingredients": ingredients
    }
    
    try:
        response = requests.post(ollama_api_url, json=payload)
        response.raise_for_status()

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to Ollama API", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
