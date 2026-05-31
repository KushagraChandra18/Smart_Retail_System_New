import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_sentiment():
    payload = {
        "text": "Products are not delivered"
    }

    response = client.post("/sentiment", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "result" in data
    assert "sentiment" in data["result"]


def test_azure_search():
    payload = {
        "query": "electronics products"
    }

    response = client.post("/azure-search", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "results" in data


def test_search_docs():
    payload = {
        "query": "low stock"
    }

    response = client.post("/search_docs", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "results" in data


def test_upload_sales():
    payload = {
        "product_id": "P101",
        "date": "2026-05-31",
        "units_sold": 120,
        "revenue": 4500,
        "store_location": "New Delhi"
    }

    response = client.post("/upload-sales", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "message" in data


def test_forecast():
    params = {
        "store": 1,
        "dept": 1,
        "temperature": 42.31,
        "fuel_price": 2.57,
        "cpi": 211.10,
        "unemployment": 8.10,
        "size": 151315,
        "is_holiday": 0,
        "month": 5,
        "week": 22,
        "day": 31,
        "lag_1": 24924.50,
        "lag_2": 23000.25,
        "rolling_mean_4": 24000.75,
        "ema_4": 24200.50
    }

    response = client.get("/forecast", params=params)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "forecasted_sales" in data


def test_detect_anomalies():
    response = client.get("/detect-anomalies")

    assert response.status_code == 200

    data = response.json()

    assert "total_anomalies" in data
    assert "anomalies" in data


def test_detect_anomalies_by_store():
    response = client.get("/detect-anomalies/1")

    assert response.status_code == 200

    data = response.json()

    assert data["store"] == 1
    assert "total_anomalies" in data
    assert "anomalies" in data


def test_azure_foundry_architecture():
    response = client.get("/azure-foundry-architecture")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


def test_data_pipeline_summary():
    response = client.get("/data-pipeline-summary")

    assert response.status_code == 200

    data = response.json()

    assert data["pipeline_status"] == "success"