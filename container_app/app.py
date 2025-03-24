import os
import boto3
import pickle
import base64
from flask import Flask, request, jsonify
from shared.logic import inference

app = Flask(__name__)

s3_client = boto3.client("s3")
BUCKET_NAME = "goldrush-main-12705"

@app.route('/pedict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        state_payload = data['StatePayload']
        model_key = state_payload["key"]
        ticker_symbol = state_payload["ticker_symbol"]
        prediction_time_window = state_payload["prediction_time_window"]
        interval = state_payload["interval"]

        # Download model from S3
        model_path = f"/tmp/{model_key}"
        s3_client.download_file(BUCKET_NAME, model_key, model_path)

        # Load the model
        with open(model_path, "rb") as model_file:
            model = pickle.loads(base64.b64decode(model_file))

        # Run inference
        result = inference(model, ticker_symbol, prediction_time_window, interval)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
