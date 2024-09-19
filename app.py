from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return 'Test, Team 1 Project for CSC395'

# POST route to accept company and ingredients data
@app.route('/submit', methods=['POST'])
def submit_data():
    # Get the JSON data from the request body
    data = request.get_json()

    # Extract 'company' and 'ingredients' from the data
    company = data.get('company')
    ingredients = data.get('ingredients')

    # Placeholder response
    response = {
        'message': 'Data received successfully!',
        'received': {
            'company': company,
            'ingredients': ingredients
        }
    }

    # Return the response as JSON
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

