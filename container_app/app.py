import os
import boto3
import pickle
import base64
from flask import Flask, request, jsonify
from shared.logic import inference

app = Flask(__name__)

# Enable development mode for auto-reloading
# app.config["DEBUG"] = True

s3_client = boto3.client("s3")
BUCKET_NAME = "goldrush-main-12705"

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    state_payload = data['StatePayload']
    model_key = state_payload["key"]
    parameters = {
        "ticker_symbol": state_payload["ticker_symbol"],
        "prediction_time_window": state_payload["prediction_time_window"],
        "interval": state_payload["interval"]
    }

    # Download model from S3 and keep it in memory
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=model_key)
        model_data = response['Body'].read()
        model = pickle.loads(base64.b64decode(model_data))
    except s3_client.exceptions.NoSuchKey:
        return jsonify({"error": "Model file not found in S3"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to download or load model: {str(e)}"}), 500

    # Run inference
    result = inference(model, parameters)

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
