"""
Standalone UK House Price Predictor
Trains a Random Forest model on realistic synthetic data and evaluates it.
For the full web app, run the backend/ Flask server and frontend/ React app.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# ── Training data (same distributions as backend/model/trainer.py) ──────────

REGIONS = {
    "London":                   600_000,
    "South East":               395_000,
    "East of England":          335_000,
    "South West":               300_000,
    "West Midlands":            248_000,
    "East Midlands":            232_000,
    "Yorkshire and The Humber": 215_000,
    "North West":               228_000,
    "North East":               178_000,
    "Wales":                    205_000,
    "Scotland":                 200_000,
}

PROPERTY_MULT = {
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


def generate_data(n: int = 8_000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        region     = rng.choice(list(REGIONS))
        prop_type  = rng.choice(list(PROPERTY_MULT))
        choices, p = BEDROOM_DIST[prop_type]
        bedrooms   = int(rng.choice(choices, p=p))
        bathrooms  = max(1, round(bedrooms * rng.uniform(0.35, 0.70)))
        sqft       = int((350 + bedrooms * 210) * rng.uniform(0.75, 1.35)
                         * (rng.uniform(1.1, 1.4) if prop_type == "detached" else 1.0))
        age        = int(rng.integers(0, 120))
        has_garden = int(prop_type != "flat" and rng.random() > 0.15
                         or prop_type == "flat" and rng.random() > 0.85)
        has_parking = int(prop_type in ("detached", "semi-detached") or rng.random() > 0.55)

        price = (
            REGIONS[region]
            * PROPERTY_MULT[prop_type]
            * (sqft / 1_200) ** 0.85
            * (1 + (bedrooms - 3) * 0.07)
            * max(0.65, 1 - age / 160)
            * (1.05 if has_garden  else 1.0)
            * (1.03 if has_parking else 1.0)
        )
        price *= rng.lognormal(0, 0.20)
        rows.append(dict(
            bedrooms=bedrooms, bathrooms=bathrooms, sqft=sqft,
            age=age, has_garden=has_garden, has_parking=has_parking,
            property_type=prop_type, region=region, price=max(55_000, price),
        ))
    return pd.DataFrame(rows)


# ── Model training ───────────────────────────────────────────────────────────

print("Generating training data (8 000 samples)…")
df = generate_data()

le_type   = LabelEncoder().fit(df["property_type"])
le_region = LabelEncoder().fit(df["region"])
df["property_type_enc"] = le_type.transform(df["property_type"])
df["region_enc"]        = le_region.transform(df["region"])

FEATURES = ["bedrooms", "bathrooms", "sqft", "age",
            "has_garden", "has_parking", "property_type_enc", "region_enc"]

X = df[FEATURES]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

print("Training Random Forest (200 estimators)…")
model = RandomForestRegressor(n_estimators=200, max_depth=16,
                               min_samples_leaf=4, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
mae    = mean_absolute_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)

print(f"\n── Test Metrics ─────────────────────────────")
print(f"  RMSE : £{rmse:>12,.0f}")
print(f"  MAE  : £{mae:>12,.0f}")
print(f"  R²   :  {r2:.4f}")

# 5-fold CV (MAE)
cv_mae = -cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error").mean()
print(f"  CV MAE (5-fold): £{cv_mae:,.0f}")


# ── Feature importances ──────────────────────────────────────────────────────

print("\n── Feature Importances ──────────────────────")
fi = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
for feat, imp in fi.items():
    print(f"  {feat:<22} {imp:.3f}")


# ── Sample predictions ───────────────────────────────────────────────────────

samples = [
    dict(bedrooms=3, bathrooms=2, sqft=1_100, age=40,
         has_garden=1, has_parking=1, property_type="terraced", region="North West"),
    dict(bedrooms=4, bathrooms=3, sqft=2_000, age=10,
         has_garden=1, has_parking=1, property_type="detached", region="South East"),
    dict(bedrooms=2, bathrooms=1, sqft=750, age=60,
         has_garden=0, has_parking=0, property_type="flat", region="London"),
]

print("\n── Sample Predictions ───────────────────────")
for s in samples:
    row = {**s,
           "property_type_enc": le_type.transform([s["property_type"]])[0],
           "region_enc":        le_region.transform([s["region"]])[0]}
    X_s  = pd.DataFrame([row])[FEATURES]
    pred = model.predict(X_s)[0]
    trees = np.array([t.predict(X_s)[0] for t in model.estimators_])
    lo    = max(50_000, pred - 1.96 * trees.std())
    hi    = pred + 1.96 * trees.std()
    print(f"  {s['bedrooms']}bd {s['property_type']:13} | {s['region']:30} "
          f"→ £{pred:>10,.0f}  (95% CI: £{lo:,.0f} – £{hi:,.0f})")


# ── Plots ────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.patch.set_facecolor("#0f172a")
for ax in axes:
    ax.set_facecolor("#1e293b")
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#334155")

# Actual vs Predicted
axes[0].scatter(y_test / 1_000, y_pred / 1_000, alpha=0.35, s=12, color="#6366f1")
lo_k = min(y_test.min(), y_pred.min()) / 1_000
hi_k = max(y_test.max(), y_pred.max()) / 1_000
axes[0].plot([lo_k, hi_k], [lo_k, hi_k], "--", color="#f59e0b", linewidth=1.5, label="Perfect fit")
axes[0].set_xlabel("Actual (£k)", color="#94a3b8")
axes[0].set_ylabel("Predicted (£k)", color="#94a3b8")
axes[0].set_title("Actual vs Predicted", color="#e2e8f0")
axes[0].legend(labelcolor="#94a3b8", facecolor="#1e293b", edgecolor="#334155")

# Feature importances
fi_sorted = fi.sort_values()
axes[1].barh(fi_sorted.index, fi_sorted.values, color="#6366f1")
axes[1].set_xlabel("Importance", color="#94a3b8")
axes[1].set_title("Feature Importances", color="#e2e8f0")

plt.tight_layout()
plt.savefig("model_evaluation.png", dpi=150, bbox_inches="tight")
print("\nChart saved → model_evaluation.png")
plt.show()
