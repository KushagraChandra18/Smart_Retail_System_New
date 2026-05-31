from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.post("/azure-search")
def azure_search(request: SearchRequest):

    mock_results = [
        {
            "product_name": "Laptop",
            "category": "Electronics",
            "stock_status": "Available"
        },
        {
            "product_name": "Smartphone",
            "category": "Electronics",
            "stock_status": "Low Stock"
        }
    ]

    return {
        "status": "success",
        "query": request.query,
        "results": mock_results
    }