from fastapi import APIRouter, HTTPException
import pandas as pd
import joblib

router = APIRouter()

model = joblib.load(
    "app/ml/anomaly_detection_model.pkl"
)


train_df = pd.read_csv("app/ml/train.csv")

features_df = pd.read_csv("app/ml/features.csv")

stores_df = pd.read_csv("app/ml/stores.csv")


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

predictions = model.predict(X)

df["Anomaly"] = predictions

# Convert:
# -1 => anomaly
# 1 => normal

df["Anomaly"] = df["Anomaly"].map({
    1: 0,
    -1: 1
})

@router.get("/detect-anomalies")
def detect_anomalies():

    try:

        anomalies = df[df["Anomaly"] == 1]

        result = anomalies[
            [
                "Store",
                "Dept",
                "Date",
                "Weekly_Sales",
                "Temperature"
            ]
        ].head(50)

        return {
            "total_anomalies": int(len(anomalies)),
            "anomalies": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/detect-anomalies/{store_id}")
def detect_store_anomalies(store_id: int):

    try:

        anomalies = df[
            (df["Anomaly"] == 1) &
            (df["Store"] == store_id)
        ]

        if anomalies.empty:

            raise HTTPException(
                status_code=404,
                detail="No anomalies found"
            )

        result = anomalies[
            [
                "Store",
                "Dept",
                "Date",
                "Weekly_Sales",
                "Temperature"
            ]
        ]

        return {
            "store": store_id,
            "total_anomalies": int(len(result)),
            "anomalies": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )