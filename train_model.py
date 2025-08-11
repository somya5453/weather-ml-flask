import os
from dataclasses import dataclass
from typing import List, Tuple

import joblib
import numpy as np
from numpy.random import default_rng
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(APP_ROOT, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "weather_model.joblib")


@dataclass
class TrainingArtifacts:
    model: RandomForestRegressor
    feature_order: List[str]
    train_mae: float
    valid_mae: float


def generate_synthetic_weather(num_samples: int = 20000, seed: int = 42) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    rng = default_rng(seed)

    # Time features
    hours = rng.integers(0, 24, size=num_samples)
    days_of_year = rng.integers(1, 366, size=num_samples)

    hour_rad = 2 * np.pi * (hours / 24.0)
    doy_rad = 2 * np.pi * (days_of_year / 365.0)

    hour_sin = np.sin(hour_rad)
    hour_cos = np.cos(hour_rad)
    doy_sin = np.sin(doy_rad)
    doy_cos = np.cos(doy_rad)

    # Baseline temperature varies by season and time of day
    seasonal_temp = 10 * doy_sin  # warmer mid-year
    diurnal_temp = 5 * hour_cos  # warmer in afternoon
    base_temp = 15 + seasonal_temp + diurnal_temp

    # Current conditions
    temp_c = base_temp + rng.normal(0, 2.0, size=num_samples)
    humidity = np.clip(70 - (temp_c - 15) * 2 + rng.normal(0, 5.0, size=num_samples), 5, 100)
    pressure_hpa = 1013 + rng.normal(0, 7.0, size=num_samples) - 0.1 * doy_cos
    wind_kph = np.clip(10 + 5 * rng.random(num_samples) + 2 * (1 - hour_cos), 0, None)
    cloud_pct = np.clip(50 + 0.5 * humidity - 0.3 * (temp_c - 15) + rng.normal(0, 10.0, size=num_samples), 0, 100)

    # Target: next-hour temperature
    temp_next_c = (
        0.7 * temp_c
        + 0.05 * humidity
        - 0.03 * (pressure_hpa - 1013)
        - 0.1 * (cloud_pct / 100.0) * (1 + 0.2 * wind_kph)
        + 0.5 * hour_sin
        + 0.3 * doy_sin
        + rng.normal(0, 1.5, size=num_samples)
    )

    feature_order = [
        "temp_c",
        "humidity",
        "pressure_hpa",
        "wind_kph",
        "cloud_pct",
        "hour_sin",
        "hour_cos",
        "doy_sin",
        "doy_cos",
    ]

    X = np.column_stack(
        [
            temp_c,
            humidity,
            pressure_hpa,
            wind_kph,
            cloud_pct,
            hour_sin,
            hour_cos,
            doy_sin,
            doy_cos,
        ]
    )
    y = temp_next_c
    return X.astype(float), y.astype(float), feature_order


def train_and_save(num_samples: int = 20000, seed: int = 42) -> TrainingArtifacts:
    X, y, feature_order = generate_synthetic_weather(num_samples=num_samples, seed=seed)

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=seed)

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        random_state=seed,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    train_mae = float(mean_absolute_error(y_train, model.predict(X_train)))
    valid_mae = float(mean_absolute_error(y_valid, model.predict(X_valid)))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({
        "model": model,
        "feature_order": feature_order,
        "metrics": {"train_mae": train_mae, "valid_mae": valid_mae},
    }, MODEL_PATH)

    return TrainingArtifacts(model=model, feature_order=feature_order, train_mae=train_mae, valid_mae=valid_mae)


if __name__ == "__main__":
    artifacts = train_and_save()
    print({
        "message": "Model trained and saved",
        "model_path": MODEL_PATH,
        "train_mae": artifacts.train_mae,
        "valid_mae": artifacts.valid_mae,
    })
