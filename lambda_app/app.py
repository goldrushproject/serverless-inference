import json
from shared.logic import inference

def lambda_handler(event, context):
    model_serialized = event["model"]
    parameters = event["parameters"]
    ticker_symbol = parameters["ticker_symbol"]
    prediction_time_window = parameters["prediction_time_window"]
    interval = parameters["interval"]

    result = inference(model_serialized, ticker_symbol, prediction_time_window, interval)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
