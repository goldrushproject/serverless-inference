import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import Polynomial

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

    # Forecast and calculate trend indices one term at a time to conserve memory
    short_term_steps = forecast_steps // 3
    mid_term_steps = 2 * forecast_steps // 3
    long_term_steps = forecast_steps

    def calculate_trend(forecast, window, degree=2):
        print(f"Calculating trend with window={window}, degree={degree}, and forecast dataset size={len(forecast)}...")
        rolling_mean = pd.Series(forecast).rolling(window=window).mean().dropna()
        print(f"Rolling mean (first 5 values): {rolling_mean.head()}")
        x = np.linspace(0, 1, len(rolling_mean))  # Normalize to range [0,1]
        print(f"x values for polynomial fit: {x[:5]} (showing first 5 values)")
        coeffs = np.polyfit(x, rolling_mean, degree)
        print(f"Polynomial coefficients: {coeffs}")
        poly = Polynomial(coeffs)
        trend = np.mean(np.gradient(poly(x)))  # Average slope over all points
        print(f"Calculated trend: {trend}")
        return trend

    # Dynamically scale window size based on forecast steps
    def calculate_window_size(steps, scale_factor=0.05, min_window=5):
        return max(int(steps * scale_factor), min_window)

    # Short term forecast and trend using polynomial fit
    short_term_forecast = model.forecast(steps=short_term_steps)
    short_term_window = calculate_window_size(short_term_steps)
    short_term_trend = calculate_trend(short_term_forecast, window=short_term_window)

    # Mid term forecast and trend using polynomial fit
    mid_term_forecast = model.forecast(steps=mid_term_steps)
    mid_term_window = calculate_window_size(mid_term_steps)
    mid_term_trend = calculate_trend(mid_term_forecast, window=mid_term_window)

    # Long term forecast and trend using polynomial fit
    long_term_forecast = model.forecast(steps=long_term_steps)
    long_term_window = calculate_window_size(long_term_steps)
    long_term_trend = calculate_trend(long_term_forecast, window=long_term_window)

    # Print the forecasted values for debugging
    print(f"Short term forecast (first 5 values): {short_term_forecast[:5]}")

    return {
        "ticker_symbol": ticker_symbol,
        "prediction_time_window": prediction_time_window,
        "interval": interval,
        "short_term_trend": short_term_trend,
        "mid_term_trend": mid_term_trend,
        "long_term_trend": long_term_trend,
    }
