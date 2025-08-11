# Weather ML Flask App

A Flask web app that predicts next-hour temperature using current weather data from Open-Meteo API and a machine learning model.

## Features
- **Automatic Weather Data**: Fetches real-time weather data from Open-Meteo API (free, no API key needed)
- **City-based Predictions**: Enter any city name to get current weather and predictions
- **Flask UI** (`/`) and **JSON API** (`/api/predict`)
- **Machine Learning Model**: RandomForestRegressor trained on synthetic weather data
- **Global Coverage**: Works with any city worldwide

## Setup

### 1. No API Key Required! 🎉
This app uses Open-Meteo API which is completely free and doesn't require any registration or API key.

### 2. Environment Setup
No environment variables needed! The app works out of the box.

### 3. Install and Run
```bash
# 1) Create venv (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Train and save model
python train_model.py

# 4) Run the app
python app.py
# Open http://localhost:5000 (or set PORT=8080 for different port)
```

## Usage

### Web Interface
1. Open the app in your browser
2. Enter a city name (e.g., "London", "New York", "Tokyo")
3. Click "Get Current Weather & Predict"
4. View current weather data and next-hour temperature prediction

### API

```http
POST /api/predict
Content-Type: application/json

{
  "city": "London"
}
```

Response:
```json
{
  "predicted_temp_c_next_hour": 22.5,
  "current_weather": {
    "temp_c": 20.5,
    "humidity": 65,
    "pressure_hpa": 1013,
    "wind_kph": 12.5,
    "cloud_pct": 45,
    "city": "London",
    "description": "scattered clouds"
  }
}
```

## Features
- **Real-time Weather Data**: Automatically fetches current weather conditions
- **Global City Support**: Works with any city worldwide
- **Beautiful UI**: Modern, responsive design with weather information display
- **API Integration**: RESTful API for programmatic access
- **Error Handling**: Graceful handling of API failures and invalid cities

## Notes
- The machine learning model uses synthetic data for demonstration
- For production use, retrain the model with real historical weather data
- OpenWeatherMap API has rate limits (1000 calls/day for free tier)
- The app automatically converts wind speed from m/s to km/h for consistency
