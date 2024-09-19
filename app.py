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



# Explanation of the Changes:

#    /submit route: This route accepts POST requests and expects the request body to contain JSON data with company and ingredients. It returns a JSON response with the data it received.
#    request.get_json(): This is used to parse the incoming JSON data.
#    Placeholder response: It responds with a message confirming that the data was received.
