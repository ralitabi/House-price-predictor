# House Price Prediction

A simple Python script to predict house prices in the UK using Linear Regression.

## Features

- Uses synthetic UK house price data
- Predicts price based on square footage and number of bedrooms
- Evaluates model performance with MSE and R-squared
- Includes visualization of actual vs predicted prices

## Requirements

Install the required packages:

```
pip install -r requirements.txt
```

## Usage

Run the script:

```
python house_price_prediction.py
```

The script will:
1. Train a linear regression model on sample data
2. Evaluate the model
3. Predict the price for a sample house (1600 sq ft, 3 bedrooms)
4. Display a scatter plot of actual vs predicted prices

## Data

The script uses synthetic data for demonstration. In a real application, you would use actual UK house price data from sources like the UK House Price Index or property websites.