<div align="center">

# 🏡 UK House Price Predictor

**Machine-learning powered property valuation with live market data**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## Overview

A full-stack property valuation tool that combines a **Random Forest ML model** with **live HM Land Registry data** to estimate UK house prices with confidence intervals. Input your property details and get an instant estimate alongside 24-month regional market trends.

---

## Features

- **Random Forest model** — 200 estimators trained on 10,000 synthetic UK property samples
- **95% confidence intervals** — derived from per-tree variance across the forest
- **Live market data** — 24-month price trends pulled from the HM Land Registry UKHPI API
- **Regional benchmarking** — compares your estimate against the regional average
- **11 UK regions · 4 property types** — detached, semi-detached, terraced, flat
- **Offline fallback** — gracefully serves estimated trend data if the API is unavailable

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML model | scikit-learn RandomForestRegressor |
| Backend API | Python · Flask · joblib |
| Data source | HM Land Registry UKHPI REST API |
| Frontend | React 18 · Vite · Tailwind CSS |
| Charts | Recharts |

---

## Project Structure

```
House Price Predictor/
├── backend/
│   ├── app.py                  # Flask REST API
│   ├── requirements.txt
│   ├── model/
│   │   ├── trainer.py          # Data generation + model training
│   │   └── predictor.py        # Inference + confidence intervals
│   └── data/
│       └── fetcher.py          # Land Registry API + fallback
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── PredictionForm.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── MarketTrends.jsx
│   │   │   └── RegionalAverages.jsx
│   │   └── services/api.js
│   └── package.json
├── house_price_prediction.py   # Standalone script (no server needed)
└── start.bat                   # One-click startup (Windows)
```

---

## Getting Started

### Quick start (Windows)

Double-click **`start.bat`** — it installs all dependencies and opens both servers automatically.

---

### Manual setup

**Backend**

```bash
cd backend
python -m pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

**Frontend** *(separate terminal)*

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

Then open **http://localhost:5173** in your browser.

> The model trains automatically on first run (~15 seconds) and is cached to disk for all subsequent starts.

---

### Standalone script

No server required — runs entirely from the terminal:

```bash
python -m pip install -r requirements.txt
python house_price_prediction.py
```

Outputs test metrics, sample predictions, and saves `model_evaluation.png`.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/predict` | Predict price for a property |
| `GET` | `/api/market-trends?region=London` | 24-month price trend for a region |
| `GET` | `/api/regional-averages` | Average prices across all 11 regions |
| `GET` | `/api/regions` | List of supported regions |
| `GET` | `/api/health` | Server + model status |

**Example request**

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "bedrooms": 3,
    "bathrooms": 2,
    "sqft": 1200,
    "property_type": "semi-detached",
    "region": "South East",
    "age": 30,
    "has_garden": 1,
    "has_parking": 1
  }'
```

**Example response**

```json
{
  "predicted_price": 302853,
  "lower_bound": 226064,
  "upper_bound": 379642,
  "price_per_sqft": 252,
  "regional_average": 392000,
  "vs_regional_avg_pct": -22.7,
  "confidence": "95%"
}
```

---

## Data & Model

Property prices are modelled from real UK regional distributions (HM Land Registry 2024 Q4 averages) with realistic noise applied. The model accounts for:

- Square footage (non-linear size scaling)
- Bedrooms & bathrooms
- Property type premium/discount
- Regional price baseline
- Property age depreciation
- Garden and parking bonuses

Live 24-month trend data is fetched from the **HM Land Registry UK House Price Index API** — no API key required.

---

## License

This project is licensed under the [MIT License](LICENSE).
