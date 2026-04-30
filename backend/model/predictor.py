import logging
import os

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "house_price_model.pkl")


class HousePricePredictor:
    def __init__(self):
        self._model = None
        self._encoders = None
        self._features = None
        self._load()

    def _load(self):
        if os.path.exists(MODEL_PATH):
            logger.info("Loading saved model from disk...")
            saved = joblib.load(MODEL_PATH)
            self._model    = saved["model"]
            self._encoders = saved["encoders"]
            self._features = saved["features"]
        else:
            logger.info("No saved model found — training a new one...")
            from .trainer import train_model
            self._model, self._encoders, self._features = train_model()

    def is_loaded(self) -> bool:
        return self._model is not None

    def predict(self, data: dict) -> dict:
        X = self._prepare(data)

        prediction = float(self._model.predict(X)[0])

        # 95 % CI via per-tree variance
        tree_preds = np.array([t.predict(X)[0] for t in self._model.estimators_])
        std = float(np.std(tree_preds))

        from data.fetcher import REGIONAL_AVERAGES
        region       = data.get("region", "London")
        regional_avg = REGIONAL_AVERAGES.get(region, prediction)

        sqft         = max(1, float(data.get("sqft", 1)))
        price_sqft   = round(prediction / sqft, 0)
        diff_pct     = round((prediction - regional_avg) / regional_avg * 100, 1)

        return {
            "predicted_price":   round(prediction, 0),
            "lower_bound":       round(max(50_000, prediction - 1.96 * std), 0),
            "upper_bound":       round(prediction + 1.96 * std, 0),
            "price_per_sqft":    price_sqft,
            "regional_average":  regional_avg,
            "vs_regional_avg_pct": diff_pct,
            "confidence":        "95%",
        }

    def _prepare(self, data: dict) -> pd.DataFrame:
        prop_type = data["property_type"].lower().replace("_", "-")
        region    = data["region"]

        known_types   = self._encoders["property_type"].classes_
        known_regions = self._encoders["region"].classes_

        if prop_type not in known_types:
            raise ValueError(
                f"Unknown property_type '{prop_type}'. Must be one of {list(known_types)}"
            )
        if region not in known_regions:
            raise ValueError(
                f"Unknown region '{region}'. Must be one of {list(known_regions)}"
            )

        row = {
            "bedrooms":         int(data["bedrooms"]),
            "bathrooms":        int(data["bathrooms"]),
            "sqft":             float(data["sqft"]),
            "age":              int(data.get("age", 30)),
            "has_garden":       int(data.get("has_garden", 0)),
            "has_parking":      int(data.get("has_parking", 0)),
            "property_type_enc": int(
                self._encoders["property_type"].transform([prop_type])[0]
            ),
            "region_enc": int(
                self._encoders["region"].transform([region])[0]
            ),
        }
        return pd.DataFrame([row])[self._features]
