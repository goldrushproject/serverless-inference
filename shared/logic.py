import pandas as pd
import numpy as np

def inference(model, parameters):
    """
    Deserialize the model, compute future time steps, and forecast future stock prices
    using the SARIMAX model's forecast method with dummy exogenous variables.

    Parameters:
        model (SARIMAXResults): A fitted SARIMAX model.
        parameters (dict): Dictionary with the following keys:
            - ticker_symbol (str): Stock ticker symbol.
            - prediction_time_window (int): Prediction window in days.
            - interval (str): Time interval for predictions ('1m', '1h', '1d').

    Returns:
        dict: A dictionary containing the ticker symbol, prediction window, interval,
              and a list of forecasted stock prices.
    """
    # Extract parameters
    ticker_symbol = parameters["ticker_symbol"]
    prediction_time_window = parameters["prediction_time_window"]
    interval = parameters["interval"]

    # Calculate the number of forecast steps based on the interval
    # For '1m': 1440 steps per day, '1h': 24 steps per day, '1d': 1 step per day
    steps_per_day = {"1m": 1440, "1h": 24, "1d": 1}.get(interval, 24)
    forecast_steps = prediction_time_window * steps_per_day

    # Use SARIMAX's forecast method to predict future stock prices
    forecast = model.forecast(steps=forecast_steps)

    return {
        "ticker_symbol": ticker_symbol,
        "prediction_time_window": prediction_time_window,
        "interval": interval,
        "predicted_prices": forecast.tolist()
    }
