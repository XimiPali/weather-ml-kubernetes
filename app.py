import requests
import numpy as np
from flask import Flask, jsonify
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Global model and data — shared between endpoints
model = None
next_day_index = None

def fetch_weather_data():
    """Fetch historical daily max temperature from Open-Meteo public API."""
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        "?latitude=40.71&longitude=-74.00"
        "&start_date=2026-04-01&end_date=2026-04-20"
        "&daily=temperature_2m_max&timezone=auto"
    )
    response = requests.get(url)
    data = response.json()
    temperatures = data["daily"]["temperature_2m_max"]
    return temperatures


@app.route("/train")
def train():
    global model, next_day_index

    temperatures = fetch_weather_data()

    # Building X (day index) and Y (temperature) arrays
    X = np.array(range(len(temperatures))).reshape(-1, 1)
    Y = np.array(temperatures)

    model = LinearRegression()
    model.fit(X, Y)

    # Remembering what the "next" day index will be for prediction
    next_day_index = len(temperatures)

    return jsonify({
        "status": "model trained",
        "days_used": len(temperatures),
        "next_day_index": next_day_index
    })


@app.route("/predict")
def predict():
    global model, next_day_index

    if model is None:
        return jsonify({"error": "Model not trained yet. Call /train first."}), 400

    # Predicting temperature for the next day
    prediction = model.predict([[next_day_index]])
    predicted_temp = round(float(prediction[0]), 2)

    return jsonify({
        "next_day_index": next_day_index,
        "predicted_temperature_celsius": predicted_temp
    })


if __name__ == "__main__":
    print("Starting Flask app...")
    print("/train   → train the model on recent weather data")
    print("/predict → get the predicted next-day temperature")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)