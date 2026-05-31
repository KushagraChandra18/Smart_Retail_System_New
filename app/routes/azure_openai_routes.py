import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

router = APIRouter()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()


class GenAIRequest(BaseModel):
    question: str


@router.post("/genai-chat")
def genai_chat(request: GenAIRequest):
    try:
        if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_DEPLOYMENT:
            raise HTTPException(
                status_code=500,
                detail="Azure OpenAI environment variables are missing"
            )

        client = OpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            base_url=AZURE_OPENAI_ENDPOINT
        )

        response = client.responses.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            input=f"""
You are an Enterprise Smart Retail AI Assistant.

Respond in a professional, conversational manner like a business consultant.
Use plain text only. Do not return JSON. Do not use markdown symbols like ** or ###.

Structure your response exactly like this:

Executive Summary

Key Insights
1. First insight
2. Second insight
3. Third insight

Recommended Actions
- First action
- Second action
- Third action

Risk Assessment

Question:
{request.question}
"""
        )

        return {
            "status": "success",
            "provider": "Azure OpenAI / Azure AI Foundry",
            "deployment": AZURE_OPENAI_DEPLOYMENT,
            "question": request.question,
            "response": response.output_text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Azure OpenAI GenAI failed: {str(e)}"
        )