from flask import Flask, request, jsonify
from shared.logic import inference

# trigger
app = Flask(__name__)

@app.route('/', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        model_serialized = data["model"]
        parameters = data["parameters"]
        ticker_symbol = parameters["ticker_symbol"]
        prediction_time_window = parameters["prediction_time_window"]
        interval = parameters["interval"]

        result = inference(model_serialized, ticker_symbol, prediction_time_window, interval)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
