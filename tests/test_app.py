import json
import unittest
from unittest.mock import patch
import requests
from app import app, request_recipe

class MockResponse:
    def __init__(self, status_code, json_data, stream=False):
        self.status_code = status_code
        self.json_data = json_data
        self.stream = stream

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"{self.status_code} Error")

    def iter_lines(self, decode_unicode=False):
        if isinstance(self.json_data, dict):
            yield json.dumps(self.json_data).encode('utf-8')
        else:
            for line in self.json_data.splitlines():
                yield line.encode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

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
        with patch('app.request_recipe', return_value={"name": "Test Recipe", "tagline": "Test tagline", "ingredients": ["Salt", "Sugar"], "instructions": ["Mix ingredients", "Serve"]}):
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

    def test_empty_ingredients_submit(self):
        """Test the /submit route with empty ingredients."""
        empty_data = {
            "company": "Nabisco",
            "ingredients": ""
        }
        response = self.app.post('/submit', json=empty_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid input. Please select a valid company and provide ingredients.', response.data)

    def test_request_recipe_success(self):
        """Test the request_recipe function with a successful response."""
        mock_response = MockResponse(200, json_data='{"response":"**Test Recipe**"}', stream=True)
        with patch('requests.post', return_value=mock_response):
            result = request_recipe("Test prompt")
            expected_result = {
                "name": "Test Recipe",
                "tagline": "",
                "ingredients": [],
                "instructions": []
            }
            self.assertEqual(result, expected_result)

    def test_request_recipe_invalid_json(self):
        """Test the request_recipe function with invalid JSON."""
        mock_response = MockResponse(200, json_data="Invalid JSON", stream=True)
        with patch('requests.post', return_value=mock_response):
            with self.assertRaises(ValueError) as context:
                request_recipe("Test prompt")
            self.assertIn("Invalid JSON structure received from the API", str(context.exception))


if __name__ == '__main__':
    unittest.main()
