import json
import pickle
import base64
from shared.logic import inference

def lambda_handler(event, context):
    model_serialized = event["model"]
    parameters = event["parameters"]

    # Deserialize the model
    model = pickle.loads(base64.b64decode(model_serialized))

    # Perform inference
    result = inference(model, parameters)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
