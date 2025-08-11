import os
from datetime import datetime
from typing import Dict, List

import numpy as np
from flask import Flask, jsonify, render_template, request
import joblib
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "models", "weather_model.joblib")

app = Flask(__name__)

# Weather API configuration - Using Open-Meteo (free, no API key needed)
WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1/forecast"


def _load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    model_bundle = joblib.load(MODEL_PATH)
    return model_bundle


MODEL_BUNDLE = _load_model()


def _get_city_coordinates(city="London"):
    """Get coordinates for a city using Open-Meteo geocoding"""
    try:
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        response = requests.get(geocoding_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("results") and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": result.get("country", "")
            }
        return None
    except Exception as e:
        print(f"Error getting coordinates for {city}: {e}")
        return None


def _get_current_weather(city="London"):
    """Fetch current weather data from Open-Meteo API"""
    try:
        # First get coordinates for the city
        coords = _get_city_coordinates(city)
        if not coords:
            return None
        
        # Get current weather data
        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,cloud_cover",
            "timezone": "auto"
        }
        
        response = requests.get(WEATHER_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data["current"]
        
        weather_data = {
            "temp_c": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "pressure_hpa": current["surface_pressure"],
            "wind_kph": current["wind_speed_10m"] * 3.6,  # Convert m/s to km/h
            "cloud_pct": current["cloud_cover"],
            "city": coords["name"],
            "country": coords["country"],
            "description": "Current weather conditions"
        }
        
        return weather_data
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        return None


def _to_float(value: str, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _cyclical_time_features(when: datetime) -> Dict[str, float]:
    hour = when.hour
    day_of_year = when.timetuple().tm_yday

    hour_rad = 2 * np.pi * (hour / 24.0)
    doy_rad = 2 * np.pi * (day_of_year / 365.0)

    return {
        "hour_sin": float(np.sin(hour_rad)),
        "hour_cos": float(np.cos(hour_rad)),
        "doy_sin": float(np.sin(doy_rad)),
        "doy_cos": float(np.cos(doy_rad)),
    }


def _build_feature_vector(
    temp_c: float,
    humidity: float,
    pressure_hpa: float,
    wind_kph: float,
    cloud_pct: float,
    when: datetime,
    feature_order: List[str],
) -> np.ndarray:
    cyc = _cyclical_time_features(when)
    feats: Dict[str, float] = {
        "temp_c": temp_c,
        "humidity": humidity,
        "pressure_hpa": pressure_hpa,
        "wind_kph": wind_kph,
        "cloud_pct": cloud_pct,
        "hour_sin": cyc["hour_sin"],
        "hour_cos": cyc["hour_cos"],
        "doy_sin": cyc["doy_sin"],
        "doy_cos": cyc["doy_cos"],
    }
    return np.array([[feats[name] for name in feature_order]], dtype=float)


@app.route("/", methods=["GET", "POST"])
def index():
    if MODEL_BUNDLE is None:
        return render_template(
            "index.html",
            prediction=None,
            error="Model not found. Please run: python train_model.py",
        )

    prediction = None
    error = None
    current_weather = None

    if request.method == "POST":
        try:
            city = request.form.get("city", "London")
            
            # Get current weather from API
            current_weather = _get_current_weather(city)
            
            if current_weather is None:
                error = "Could not fetch current weather data. Please check your API key or try again."
                return render_template("index.html", prediction=prediction, error=error, current_weather=current_weather)
            
            # Use API data for prediction
            temp_c = current_weather["temp_c"]
            humidity = current_weather["humidity"]
            pressure_hpa = current_weather["pressure_hpa"]
            wind_kph = current_weather["wind_kph"]
            cloud_pct = current_weather["cloud_pct"]
            when = datetime.now()

            X = _build_feature_vector(
                temp_c,
                humidity,
                pressure_hpa,
                wind_kph,
                cloud_pct,
                when,
                MODEL_BUNDLE["feature_order"],
            )
            y_pred = float(MODEL_BUNDLE["model"].predict(X)[0])
            prediction = {
                "predicted_temp_c_next_hour": round(y_pred, 2),
            }
        except Exception as ex:
            error = f"Prediction error: {ex}"

    return render_template("index.html", prediction=prediction, error=error, current_weather=current_weather)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    if MODEL_BUNDLE is None:
        return jsonify({"error": "Model not found. Run 'python train_model.py' first."}), 400

    data = request.get_json(silent=True) or {}

    try:
        city = data.get("city", "London")
        
        # Get current weather from API
        current_weather = _get_current_weather(city)
        
        if current_weather is None:
            return jsonify({"error": "Could not fetch current weather data"}), 400
        
        # Use API data for prediction
        temp_c = current_weather["temp_c"]
        humidity = current_weather["humidity"]
        pressure_hpa = current_weather["pressure_hpa"]
        wind_kph = current_weather["wind_kph"]
        cloud_pct = current_weather["cloud_pct"]
        when = datetime.now()

        X = _build_feature_vector(
            temp_c,
            humidity,
            pressure_hpa,
            wind_kph,
            cloud_pct,
            when,
            MODEL_BUNDLE["feature_order"],
        )
        y_pred = float(MODEL_BUNDLE["model"].predict(X)[0])
        
        return jsonify({
            "predicted_temp_c_next_hour": y_pred,
            "current_weather": current_weather
        })
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

# For Vercel deployment
app.debug = False
