from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    company = data.get("company")
    ingredients = data.get("ingredients")

    if company and ingredients:
        recipe = {
            "company": company,
            "ingredients": ingredients,
            "recipe": f"Here is a recipe from {company} using {', '.join(ingredients)}."
        }
    else:
        recipe = {
            "error": "Missing company or ingredients in the request."
        }
    
    return jsonify(recipe)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
