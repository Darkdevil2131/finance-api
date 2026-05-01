from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# ✅ CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    query: str


# 🔥 AI-like smart parser (improved logic)
def smart_finance_agent(query):
    text = query.lower()
    numbers = list(map(float, re.findall(r'\d+', text)))

    results = []

    # PROFIT MARGIN
    if "revenue" in text and "profit" in text and len(numbers) >= 2:
        revenue, profit = numbers[0], numbers[1]
        margin = (profit / revenue) * 100
        results.append({
            "metric": "profit_margin",
            "value": round(margin, 2),
            "formula": "Profit / Revenue"
        })

    # ROI (better logic now)
    if "investment" in text and ("gain" in text or "return" in text):
        if len(numbers) >= 2:
            investment, gain = numbers[0], numbers[1]
            roi = ((gain - investment) / investment) * 100
            results.append({
                "metric": "roi",
                "value": round(roi, 2),
                "formula": "(Gain - Investment) / Investment"
            })

    # GROWTH
    if "old" in text and "new" in text and len(numbers) >= 2:
        old, new = numbers[0], numbers[1]
        growth = ((new - old) / old) * 100
        results.append({
            "metric": "growth",
            "value": round(growth, 2),
            "formula": "(New - Old) / Old"
        })

    if results:
        return {"results": results}

    return {"error": "Could not understand input"}


# API route
@app.post("/analyze")
def analyze(request: QueryRequest):
    return smart_finance_agent(request.query)


# Health check (🔥 MLOps best practice)
@app.get("/")
def home():
    return {"message": "Finance AI Agent is running"}