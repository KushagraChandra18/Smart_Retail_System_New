import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

router = APIRouter()

TEXT_ANALYTICS_ENDPOINT = os.getenv("TEXT_ANALYTICS_ENDPOINT")
TEXT_ANALYTICS_KEY = os.getenv("TEXT_ANALYTICS_KEY")


class SentimentRequest(BaseModel):
    text: str


@router.post("/sentiment")
def sentiment_analysis(request: SentimentRequest):
    try:
        if not TEXT_ANALYTICS_ENDPOINT or not TEXT_ANALYTICS_KEY:
            raise HTTPException(
                status_code=500,
                detail="TEXT_ANALYTICS_ENDPOINT or TEXT_ANALYTICS_KEY missing"
            )

        client = TextAnalyticsClient(
            endpoint=TEXT_ANALYTICS_ENDPOINT,
            credential=AzureKeyCredential(TEXT_ANALYTICS_KEY)
        )

        result = client.analyze_sentiment([request.text])[0]

        return {
            "status": "success",
            "text": request.text,
            "result": {
                "sentiment": result.sentiment,
                "positive_score": result.confidence_scores.positive,
                "neutral_score": result.confidence_scores.neutral,
                "negative_score": result.confidence_scores.negative
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )