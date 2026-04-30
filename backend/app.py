from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

_predictor = None
_fetcher = None


def get_predictor():
    global _predictor
    if _predictor is None:
        from model.predictor import HousePricePredictor
        _predictor = HousePricePredictor()
    return _predictor


def get_fetcher():
    global _fetcher
    if _fetcher is None:
        from data.fetcher import MarketDataFetcher
        _fetcher = MarketDataFetcher()
    return _fetcher


@app.route("/api/health", methods=["GET"])
def health():
    predictor = get_predictor()
    return jsonify({"status": "ok", "model_loaded": predictor.is_loaded()})


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required = ["bedrooms", "bathrooms", "sqft", "property_type", "region"]
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        result = get_predictor().predict(data)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error("Prediction error", exc_info=True)
        return jsonify({"error": "Prediction failed. Please try again."}), 500


@app.route("/api/market-trends", methods=["GET"])
def market_trends():
    try:
        region = request.args.get("region", "england")
        data = get_fetcher().fetch_price_trends(region)
        return jsonify(data)
    except Exception as e:
        logger.error("Market data error", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/regional-averages", methods=["GET"])
def regional_averages():
    try:
        data = get_fetcher().fetch_regional_averages()
        return jsonify(data)
    except Exception as e:
        logger.error("Regional averages error", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("Loading model on startup...")
    get_predictor()
    logger.info("Starting server on http://localhost:5000")
    app.run(debug=True, port=5000, host="0.0.0.0")
