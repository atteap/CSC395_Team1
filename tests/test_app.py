import json
import unittest
from unittest.mock import patch, Mock
import requests
from app import app, request_recipe

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the index route to check if companies are correctly loaded."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nabisco', response.data)

    def test_valid_submit(self):
        """Test the /submit route with valid data."""
        valid_data = {
            "company": "Nabisco",
            "ingredients": "Salt, Sugar"
        }
        with patch('app.request_recipe', return_value={"name": "Test Recipe"}):
            response = self.app.post('/submit', json=valid_data)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("name", data)
            self.assertEqual(data["name"], "Test Recipe")

    def test_invalid_company_submit(self):
        """Test the /submit route with an invalid company."""
        invalid_data = {
            "company": "InvalidCompany",
            "ingredients": "Salt, Sugar"
        }
        response = self.app.post('/submit', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid company', response.data)

    def test_malformed_json_submit(self):
        """Test the /submit route with malformed JSON input."""
        malformed_data = "{company: Nabisco, ingredients: Salt, Sugar"  # Missing closing brace
        response = self.app.post('/submit', data=malformed_data, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Malformed JSON', response.data)

    @patch('app.requests.post')  # Ensure correct patching path
    def test_request_recipe_success(self, mock_post):
        """Test successful recipe generation from Ollama API."""
        # Create a mock response object that simulates a successful API call
        mock_response = Mock()
        mock_response.status_code = 200

        # Provide a structured response string in multiple chunks to simulate streaming behavior
        mock_response.iter_lines.return_value = iter([
            json.dumps({"response": "**Recipe Name**"}).encode('utf-8'),
            json.dumps({"response": "**Tagline:** \"Catchy tagline here!\""}).encode('utf-8'),
            json.dumps({"response": "**Ingredients:**"}).encode('utf-8'),
            json.dumps({"response": "- Ingredient 1"}).encode('utf-8'),
            json.dumps({"response": "- Ingredient 2"}).encode('utf-8'),
            json.dumps({"response": "**Instructions:**"}).encode('utf-8'),
            json.dumps({"response": "1. Step one."}).encode('utf-8'),
            json.dumps({"response": "2. Step two."}).encode('utf-8'),
            json.dumps({"done": True}).encode('utf-8')
        ])

        # Set up the mock to behave like a context manager
        mock_post.return_value.__enter__.return_value = mock_response

        # Call the function under test
        recipe = request_recipe("Test prompt")

        # Check that the expected fields are in the response
        self.assertIn("name", recipe)
        self.assertIn("tagline", recipe)
        self.assertIn("ingredients", recipe)
        self.assertIn("instructions", recipe)

        # Verify that the parsed values match the expected results
        self.assertEqual(recipe["name"], "Recipe Name")
        self.assertEqual(recipe["tagline"], "Catchy tagline here!")
        self.assertEqual(recipe["ingredients"], ["Ingredient 1", "Ingredient 2"])
        self.assertEqual(recipe["instructions"], ["Step one.", "Step two."])

    @patch('app.requests.post')  # Ensure correct patching path
    def test_request_recipe_timeout(self, mock_post):
        """Test handling of a timeout from the Ollama API."""
        mock_post.side_effect = requests.exceptions.Timeout
        with self.assertRaises(ValueError):
            request_recipe("Test prompt")

    @patch('app.requests.post')  # Ensure correct patching path
    def test_request_recipe_failure(self, mock_post):
        """Test handling of a failed request to the Ollama API."""
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        with self.assertRaises(ValueError):
            request_recipe("Test prompt")

if __name__ == '__main__':
    unittest.main()
