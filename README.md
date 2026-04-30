<div align="center">

# UK House Price Predictor

Machine learning–powered property valuation tool with live UK market data.

<br/>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4%2B-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## Overview

UK House Price Predictor is a full-stack application that estimates residential property values using a Random Forest machine learning model combined with live market data from the HM Land Registry.

Users can input property details to receive:

- An instant price estimate
- A 95% confidence interval
- Regional comparisons
- 24-month market trend insights

The system is designed to demonstrate practical applications of machine learning in real-world property valuation.

---

## Key Features

**Machine Learning Model**
- Random Forest model with 200 estimators
- Trained on 10,000 synthetic UK property samples
- Captures non-linear relationships in housing data

**Price Estimation**
- Instant predictions based on user input
- 95% confidence intervals derived from tree variance
- Price-per-square-foot calculation

**Market Insights**
- Live 24-month regional trends
- Regional benchmarking against average prices
- Support for 11 UK regions

**Property Coverage**
- Detached, semi-detached, terraced, flats

**Reliability**
- Offline fallback when external API is unavailable
- Model caching for faster performance after first run

---

## Technology Stack

| Layer | Technology |
|---|---|
| Machine Learning | scikit-learn (RandomForestRegressor) |
| Backend | Python, Flask, joblib |
| Data Source | HM Land Registry UKHPI API |
| Frontend | React, Vite, Tailwind CSS |
| Visualisation | Recharts |

---

## Project Structure

```
House Price Predictor/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model/
│   │   ├── trainer.py
│   │   └── predictor.py
│   └── data/
│       └── fetcher.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── services/
│   └── package.json
│
├── house_price_prediction.py
└── start.bat
```

---

## Getting Started

### Quick Start (Windows)

Run the following file to automatically install dependencies and start both servers:

```
start.bat
```

---

### Manual Setup

**Backend**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend runs at `http://localhost:5000`

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

### Standalone Mode

Run without a server:

```bash
pip install -r requirements.txt
python house_price_prediction.py
```

Outputs:
- Model evaluation metrics
- Sample predictions
- Visual performance plots

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/predict` | Predict property price |
| `GET` | `/api/market-trends` | Get 24-month regional trends |
| `GET` | `/api/regional-averages` | Compare regional averages |
| `GET` | `/api/regions` | List supported regions |
| `GET` | `/api/health` | Check system status |

**Example Request**

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

**Example Response**

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

## Data and Model

The model is trained on synthetic data derived from real UK regional price distributions (HM Land Registry 2024 data). It considers:

- Property size (square footage)
- Number of bedrooms and bathrooms
- Property type
- Regional pricing differences
- Property age
- Additional features such as garden and parking

Live market trends are retrieved from the HM Land Registry UK House Price Index API. No API key is required.

---

## Design Considerations

- Efficient model inference with cached training
- Separation of backend and frontend components
- API-driven architecture
- Robust fallback mechanisms for data reliability

---

## Future Improvements

- Integration with real transaction datasets
- More advanced models (e.g. Gradient Boosting, XGBoost)
- User authentication and saved predictions
- Deployment to cloud platforms
- Enhanced UI and analytics dashboard

---

## License

This project is licensed under the [MIT License](LICENSE).
