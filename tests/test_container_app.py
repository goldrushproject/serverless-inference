import unittest
import json
import base64
import pickle
from unittest.mock import patch, MagicMock
from container_app.app import app 

class TestApp(unittest.TestCase):
    def setUp(self):
        # This will create a test client for our app
        self.client = app.test_client()

    @patch('boto3.client')
    def test_app(self, mock_boto_client):
        # Mock the S3 client and its download_file method
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        
        # Mock the behavior of downloading a file from S3
        # Instead of actually downloading, we will simulate loading the model
        with open('tests/trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        model_serialized = base64.b64encode(pickle.dumps(model)).decode('utf-8')
        
        # Mock the download_file call to simulate loading a model
        def mock_download_file(Bucket, Key, Filename):
            with open(Filename, 'wb') as f:
                f.write(base64.b64decode(model_serialized))
        
        mock_s3_client.download_file.side_effect = mock_download_file

        # Prepare the test payload
        test_payload = {
            "StatePayload": {
                "key": model_serialized,  # Assuming the Flask app receives a base64 model
                "ticker_symbol": "AAPL",
                "prediction_time_window": 10,
                "interval": "1d"
            }
        }

        # Send a POST request to the /predict endpoint
        response = self.client.post('/predict', 
                                    data=json.dumps(test_payload),
                                    content_type='application/json')

        # Get the response body as JSON
        response_body = json.loads(response.data)

        # Optionally, write out the predicted results for inspection
        with open('sample_predicted_prices.json', 'w') as f:
            json.dump(response_body['predicted_prices'], f)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Optionally, check if the response contains a specific field
        self.assertIn('predicted_prices', response_body)

if __name__ == "__main__":
    unittest.main()
