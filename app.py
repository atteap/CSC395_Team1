from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Test, Team 1 Project for CSC395' 

if __name__ == '__main__':
    app.run(debug=True)

