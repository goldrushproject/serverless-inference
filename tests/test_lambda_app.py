import unittest
import json
import base64
import pickle
from lambda_app.app import lambda_handler


class TestApp(unittest.TestCase):
    def test_app(self):
        with open('tests/trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        model_serialized = base64.b64encode(pickle.dumps(model)).decode('utf-8')

        test_event = {
            "StatePayload": {
                "key": "models/default/TSLA/114514.pkl",
                "model": None,
                "ticker_symbol": "TSLA",
                "prediction_time_window": 1,
                "interval": "1m"
            },
        }
        context = {}
        response = lambda_handler(test_event, context)
        response_body = json.loads(response['body'])

        with open('predicted_data.json', 'w') as f:
            print(response_body)
            json.dump(response_body, f)
        
        self.assertEqual(response["statusCode"], 200)

if __name__ == "__main__":
    unittest.main()
