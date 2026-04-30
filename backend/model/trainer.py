import os
import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

logger = logging.getLogger(__name__)

REGIONS = {
    "London":                         {"base": 600_000, "noise": 0.28},
    "South East":                     {"base": 395_000, "noise": 0.22},
    "East of England":                {"base": 335_000, "noise": 0.20},
    "South West":                     {"base": 300_000, "noise": 0.20},
    "West Midlands":                  {"base": 248_000, "noise": 0.18},
    "East Midlands":                  {"base": 232_000, "noise": 0.17},
    "Yorkshire and The Humber":       {"base": 215_000, "noise": 0.17},
    "North West":                     {"base": 228_000, "noise": 0.17},
    "North East":                     {"base": 178_000, "noise": 0.15},
    "Wales":                          {"base": 205_000, "noise": 0.17},
    "Scotland":                       {"base": 200_000, "noise": 0.17},
}

PROPERTY_MULTIPLIERS = {
    "detached":      1.45,
    "semi-detached": 1.00,
    "terraced":      0.85,
    "flat":          0.70,
}

BEDROOM_DIST = {
    "flat":          ([1, 2, 3],    [0.35, 0.50, 0.15]),
    "terraced":      ([2, 3, 4],    [0.30, 0.50, 0.20]),
    "semi-detached": ([2, 3, 4, 5], [0.20, 0.45, 0.25, 0.10]),
    "detached":      ([3, 4, 5, 6], [0.20, 0.38, 0.30, 0.12]),
}


def generate_training_data(n_samples: int = 10_000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    regions = list(REGIONS.keys())
    prop_types = list(PROPERTY_MULTIPLIERS.keys())
    rows = []

    for _ in range(n_samples):
        region = rng.choice(regions)
        prop_type = rng.choice(prop_types)
        info = REGIONS[region]

        choices, probs = BEDROOM_DIST[prop_type]
        bedrooms = int(rng.choice(choices, p=probs))
        bathrooms = max(1, round(bedrooms * rng.uniform(0.35, 0.70)))

        base_sqft = 350 + bedrooms * 210
        if prop_type == "detached":
            base_sqft *= rng.uniform(1.10, 1.40)
        sqft = int(base_sqft * rng.uniform(0.75, 1.35))

        age = int(rng.integers(0, 120))
        has_garden = int(
            (prop_type != "flat" and rng.random() > 0.15)
            or (prop_type == "flat" and rng.random() > 0.85)
        )
        has_parking = int(
            prop_type in ("detached", "semi-detached") or rng.random() > 0.55
        )

        price = (
            info["base"]
            * PROPERTY_MULTIPLIERS[prop_type]
            * (sqft / 1_200) ** 0.85
            * (1 + (bedrooms - 3) * 0.07)
            * max(0.65, 1 - age / 160)
            * (1.05 if has_garden else 1.0)
            * (1.03 if has_parking else 1.0)
        )
        price *= rng.lognormal(0, info["noise"])
        price = max(55_000, price)

        rows.append({
            "bedrooms":     bedrooms,
            "bathrooms":    bathrooms,
            "sqft":         sqft,
            "age":          age,
            "has_garden":   has_garden,
            "has_parking":  has_parking,
            "property_type": prop_type,
            "region":       region,
            "price":        price,
        })

    return pd.DataFrame(rows)


FEATURE_COLS = [
    "bedrooms", "bathrooms", "sqft", "age",
    "has_garden", "has_parking", "property_type_enc", "region_enc",
]


def train_model():
    logger.info("Generating %d training samples...", 10_000)
    df = generate_training_data()

    le_type   = LabelEncoder().fit(df["property_type"])
    le_region = LabelEncoder().fit(df["region"])
    encoders  = {"property_type": le_type, "region": le_region}

    df["property_type_enc"] = le_type.transform(df["property_type"])
    df["region_enc"]        = le_region.transform(df["region"])

    X = df[FEATURE_COLS]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    logger.info("Training Random Forest (200 trees)...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=16,
        min_samples_leaf=4,
        n_jobs=-1,
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae  = mean_absolute_error(y_test, y_pred)
    r2   = r2_score(y_test, y_pred)
    logger.info("Test RMSE: £%s  MAE: £%s  R²: %.3f",
                f"{rmse:,.0f}", f"{mae:,.0f}", r2)

    model_path = os.path.join(os.path.dirname(__file__), "house_price_model.pkl")
    joblib.dump({"model": model, "encoders": encoders, "features": FEATURE_COLS}, model_path)
    logger.info("Model saved to %s", model_path)

    return model, encoders, FEATURE_COLS
