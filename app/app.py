import json
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle
import base64

def lambda_handler(event, context):

    # Extract parameters
    max_time_window = event.get("max_time_window", 1)
    ticker_symbol = event.get("ticker_symbol", "AAPL")
    interval = event.get("interval", "1h")
    future_time_window = event.get("future_time_window", 5)
    model_serialized = event.get("model", None)

    print(f"Max Time Window: {max_time_window}")
    print(f"Ticker Symbol: {ticker_symbol}")
    print(f"Interval: {interval}")

    # Deserialize the model
    if model_serialized:
        model = pickle.loads(base64.b64decode(model_serialized))
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Model not provided in the event"})
        }

    # Predict future stock prices
    future_times = pd.DataFrame(np.arange(future_time_window), columns=['Time'])
    future_prices = model.predict(future_times)

    # Example processing
    message = f"Hello from Lambda! Received ticker {ticker_symbol} with a time window of {max_time_window} and interval {interval}."

    # Return a response
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
                "max_time_window": max_time_window,
                "ticker_symbol": ticker_symbol,
                "interval": interval,
                "predicted_prices": future_prices.tolist()
            }
        ),
    }
