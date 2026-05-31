from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.sales_routes import router as sales_router
from app.routes.anomaly_routes import router as anomaly_router
from app.routes.sentiment_routes import router as sentiment_router
from app.routes.agent_routes import router as agent_router
from app.routes.search_docs_routes import router as search_docs_router
from app.routes.azure_openai_routes import router as azure_openai_router
from app.routes.azure_search_routes import router as azure_search_router
from app.routes.azure_foundry_routes import router as azure_foundry_router
from app.routes.document_intelligence_routes import router as document_intelligence_router
from app.routes.data_engineering_routes import router as data_engineering_router

tags_metadata = [
    {
        "name": "A. Python Fullstack (Backend + APIs)",
        "description": "Backend APIs, database integration, logging, error handling and testing."
    },
    {
        "name": "B. Machine Learning / Deep Learning",
        "description": "Machine learning models, training, evaluation and inference services."
    },
    {
        "name": "C. GenAI / Agents",
        "description": "Multi-agent orchestration, embeddings, vector retrieval and knowledge assistance."
    },
    {
        "name": "D. Azure AI & Cloud",
        "description": "Azure cloud services, AI integrations and deployment components."
    },
    {
        "name": "E. Data Engineering Pipeline",
        "description": "Raw → Staged → Curated ETL and analytics data pipeline."
    },
    {
        "name": "System",
        "description": "Application status and health monitoring endpoints."
    }
]

app = FastAPI(
    title="Smart Retail Assistant API",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    sales_router,
    tags=["A. Python Fullstack (Backend + APIs)"]
)

app.include_router(
    anomaly_router,
    tags=["B. Machine Learning / Deep Learning"]
)

app.include_router(
    sentiment_router,
    tags=["B. Machine Learning / Deep Learning"]
)

app.include_router(
    agent_router,
    tags=["C. GenAI / Agents"]
)

app.include_router(
    search_docs_router,
    tags=["C. GenAI / Agents"]
)

app.include_router(
    azure_openai_router,
    tags=["D. Azure AI & Cloud"]
)

app.include_router(
    azure_search_router,
    tags=["D. Azure AI & Cloud"]
)

app.include_router(
    azure_foundry_router,
    tags=["D. Azure AI & Cloud"]
)

app.include_router(
    document_intelligence_router,
    tags=["D. Azure AI & Cloud"]
)

app.include_router(
    data_engineering_router,
    tags=["E. Data Engineering Pipeline"]
)

@app.get("/", tags=["System"])
def home():
    return {
        "status": "running",
        "project": "Smart Retail Assistant",
        "version": "1.0.0"
    }

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "message": "Smart Retail Assistant API is working successfully"
    }