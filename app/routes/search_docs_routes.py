from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SearchDocsRequest(BaseModel):
    query: str


@router.post("/search_docs")
def search_docs(request: SearchDocsRequest):

    documents = [
        {
            "title": "Inventory Policy",
            "content": "Low stock products should be reordered when inventory falls below the threshold level."
        },
        {
            "title": "Customer Feedback Policy",
            "content": "Negative customer feedback should be reviewed by the store manager within 24 hours."
        },
        {
            "title": "Sales Forecasting Guide",
            "content": "Demand forecasting helps predict future sales and optimize inventory planning."
        }
    ]

    matched_results = []

    for doc in documents:
        if request.query.lower() in doc["content"].lower() or request.query.lower() in doc["title"].lower():
            matched_results.append(doc)

    if not matched_results:
        matched_results = documents[:2]

    return {
        "status": "success",
        "query": request.query,
        "results": matched_results,
        "architecture": "RAG-ready document retrieval using Azure AI Search pattern"
    }