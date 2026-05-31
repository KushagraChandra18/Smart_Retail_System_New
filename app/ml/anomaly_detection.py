import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest


train_df = pd.read_csv("app/ml/train.csv")

features_df = pd.read_csv("app/ml/features.csv")

stores_df = pd.read_csv("app/ml/stores.csv")

print("\nDatasets Loaded Successfully!")

df = train_df.merge(
    features_df,
    on=["Store", "Date", "IsHoliday"],
    how="left"
)

df = df.merge(
    stores_df,
    on="Store",
    how="left"
)

print("\nMerged Dataset Shape:", df.shape)

df.fillna(0, inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.month

df["Week"] = df["Date"].dt.isocalendar().week.astype(int)

df["Type"] = df["Type"].map({
    "A": 1,
    "B": 2,
    "C": 3
})

features = [
    "Store",
    "Dept",
    "Weekly_Sales",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
    "Size",
    "Month",
    "Week"
]

X = df[features]

print("\nTraining Isolation Forest...")

model = IsolationForest(
    n_estimators=100,
    contamination=0.02,
    random_state=42
)

model.fit(X)



df["Anomaly"] = model.predict(X)

# Convert:
# -1 => anomaly
#  1 => normal

df["Anomaly"] = df["Anomaly"].map({
    1: 0,
    -1: 1
})

anomalies = df[df["Anomaly"] == 1]

print("\nTotal Anomalies Detected:", len(anomalies))

print("\nSample Anomalies")
print("---------------------------")

print(
    anomalies[
        [
            "Store",
            "Dept",
            "Date",
            "Weekly_Sales",
            "Temperature"
        ]
    ].head(10)
)

joblib.dump(
    model,
    "app/ml/anomaly_detection_model.pkl"
)

print("\nAnomaly Detection Model Saved Successfully!")