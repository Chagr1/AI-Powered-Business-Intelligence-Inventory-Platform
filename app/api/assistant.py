import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from groq import Groq

from app.db.database import get_db
from app.models.user import User
from app.api.dependencies import require_role
from app.api.analytics import get_sales_summary, get_top_products

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

class PromptRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_business_assistant(
    request: PromptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    """Answers business questions based on real-time database analytics."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Groq API key is missing.")

    client = Groq(api_key=api_key)


    summary = get_sales_summary(db=db, current_user=current_user)
    top_products = get_top_products(limit=5, db=db, current_user=current_user)


    system_prompt = f"""
    You are an expert AI Business Assistant for an enterprise platform.
    Use the following real-time analytics data to answer the manager's questions.
    Be concise, professional, and provide actionable insights. Do not hallucinate data.

    CURRENT LIVE DATA:
    Total Revenue: ${summary['total_revenue']}
    Total Orders: {summary['total_orders']}
    Top Selling Products (Name, Total Sold, Revenue): 
    {top_products}
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.question}
            ],
            model="openai/gpt-oss-20b",
            temperature=0.3,
        )
        return {"answer": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")