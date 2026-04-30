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

# -------------------------
# Request schema
# -------------------------
class QueryRequest(BaseModel):
    query: str


# -------------------------
# Smart extraction
# -------------------------
def extract_value(text, keyword):
    pattern = rf"{keyword}\s*(\d+)"
    match = re.search(pattern, text)
    return float(match.group(1)) if match else None


# -------------------------
# Core logic
# -------------------------
def smart_finance_agent(query):
    text = query.lower()

    results = []

    # PROFIT MARGIN
    revenue = extract_value(text, "revenue")
    profit = extract_value(text, "profit")

    if revenue and profit:
        margin = (profit / revenue) * 100
        results.append({
            "metric": "profit_margin",
            "value": round(margin, 2),
            "formula": "Profit / Revenue"
        })

    # ROI
    investment = extract_value(text, "investment")
    gain = extract_value(text, "gain") or extract_value(text, "return")

    if investment and gain:
        roi = (gain / investment) * 100
        results.append({
            "metric": "roi",
            "value": round(roi, 2),
            "formula": "Gain / Investment"
        })

    # GROWTH
    old = extract_value(text, "old")
    new = extract_value(text, "new")

    if old and new:
        growth = ((new - old) / old) * 100
        results.append({
            "metric": "growth",
            "value": round(growth, 2),
            "formula": "(New - Old) / Old"
        })

    if results:
        return {"results": results}

    return {"error": "Could not understand input"}


# -------------------------
# API endpoint
# -------------------------
@app.post("/analyze")
def analyze(request: QueryRequest):
    return smart_finance_agent(request.query)