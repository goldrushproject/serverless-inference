import unittest
import json
import base64
import pickle
from app.app import lambda_handler

class TestApp(unittest.TestCase):
    def test_app(self):
        with open('tests/trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        model_serialized = base64.b64encode(pickle.dumps(model)).decode('utf-8')

        test_event = {
            "ticker_symbol": "AAPL",
            "interval": "1m",
            "prediction_time_window": 5,
            "model": model_serialized,
        }
        context = {}
        response = lambda_handler(test_event, context)
        response_body = json.loads(response['body'])
        
        with open('sample_predicted_prices.json', 'w') as f:
            # print(response_body['predicted_prices'])
            json.dump(response_body['predicted_prices'], f)
        
        self.assertEqual(response["statusCode"], 200)

if __name__ == "__main__":
    unittest.main()
