import json
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle
import base64

def lambda_handler(event, context):

    # Extract parameters
    ticker_symbol = event.get("ticker_symbol", "AAPL")
    prediction_time_window = event.get("prediction_time_window", 5)
    interval = event.get("interval", "1h")
    model_serialized = event.get("model", None)

    # Deserialize the model
    if model_serialized:
        model = pickle.loads(base64.b64decode(model_serialized))
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Model not provided in the event"})
        }

    # Calculate the step size based on the interval
    interval_mapping = {"1m": 1, "1h": 60, "1d": 1440}
    step_size = interval_mapping.get(interval, 60)

    # Predict future stock prices
    future_times = pd.DataFrame(np.arange(0, prediction_time_window * 1440, step_size), columns=['Time'])
    future_prices = model.predict(future_times)

    # Return a response
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "ticker_symbol": ticker_symbol,
                "prediction_time_window": prediction_time_window,
                "interval": interval,
                "predicted_prices": future_prices.tolist()
            }
        ),
    }