import json
import pickle
import base64
import boto3
from shared.logic import inference

s3_client = boto3.client('s3')
BUCKET_NAME = "goldrush-main-12705"

def lambda_handler(event, context):

    state_payload = event['StatePayload']
    parameters = {
        "ticker_symbol": state_payload["ticker_symbol"],
        "prediction_time_window": state_payload["prediction_time_window"],
        "interval": state_payload["interval"]
    }

    model_serialized = None
    model = None

    # Deserialize the model if model is in event
    if "model" in state_payload and state_payload["model"] is not None:
        print("Loading model from event")
        model_serialized = state_payload["model"]
    else:
        print("Loading model from S3")
        # Load the model from S3
        try:
            model_key = state_payload["key"]
        except KeyError:
            print("Model key not found in state payload, trying to find it in event")
            model_key = event['key']
        
        # Download model from S3 and keep it in memory
        try:
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=model_key)
            model_serialized = response['Body'].read()
        except s3_client.exceptions.NoSuchKey:
            print(f"Model file not found in S3: {model_key}")
            {
                "statusCode": 404,
                "body": json.dumps({"error": "Model file not found in S3"})
            }
        except Exception as e:
            print(f"Failed to download or load model: {str(e)}")
            {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to download or load model: {str(e)}"})
            }
    
    model = pickle.loads(base64.b64decode(model_serialized))

    # Perform inference
    print(parameters)
    result = inference(model, parameters)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
