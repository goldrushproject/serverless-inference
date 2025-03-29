import pandas as pd
import numpy as np

def inference(model, parameters):
    """
    Deserialize the model, compute future times, and predict stock prices.

    Parameters:
        model (str): Deserialized model.
        ticker_symbol (str): Stock ticker symbol.
        prediction_time_window (int): Time window for predictions (in days).
        interval (str): Time interval for predictions ('1m', '1h', '1d').

    Returns:
        dict: Dictionary containing ticker symbol, prediction window, interval,
              and a list of predicted prices.
    """
    # Extract parameters
    ticker_symbol = parameters["ticker_symbol"]
    prediction_time_window = parameters["prediction_time_window"]
    interval = parameters["interval"]

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
