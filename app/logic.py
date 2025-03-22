import pandas as pd
import numpy as np
import pickle
import base64

def inference(model_serialized, ticker_symbol, prediction_time_window, interval):
    """
    Deserialize the model, compute future times, and predict stock prices.

    Parameters:
        model_serialized (str): Base64 encoded serialized model.
        ticker_symbol (str): Stock ticker symbol.
        prediction_time_window (int): Time window for predictions (in days).
        interval (str): Time interval for predictions ('1m', '1h', '1d').

    Returns:
        dict: Dictionary containing ticker symbol, prediction window, interval,
              and a list of predicted prices.
    """
    # Deserialize the model
    model = pickle.loads(base64.b64decode(model_serialized))

    # Calculate the step size based on the interval
    interval_mapping = {"1m": 1, "1h": 60, "1d": 1440}
    step_size = interval_mapping.get(interval, 60)

    # Generate future times DataFrame (Time in minutes)
    future_times = pd.DataFrame(
        np.arange(0, prediction_time_window * 1440, step_size),
        columns=['Time']
    )

    # Predict future stock prices
    future_prices = model.predict(future_times)

    return {
        "ticker_symbol": ticker_symbol,
        "prediction_time_window": prediction_time_window,
        "interval": interval,
        "predicted_prices": future_prices.tolist()
    }
