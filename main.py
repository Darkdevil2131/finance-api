from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# -----------------------------
# CORS (VERY IMPORTANT for frontend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Schema
# -----------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------
# Smart Finance Agent
# -----------------------------
def smart_finance_agent(query: str):
    text = query.lower()

    # extract numbers
    numbers = list(map(float, re.findall(r'\d+', text)))

    results = []

    # -----------------------------
    # PROFIT MARGIN
    # -----------------------------
    if "revenue" in text and "profit" in text and len(numbers) >= 2:
        revenue, profit = numbers[0], numbers[1]
        if revenue != 0:
            margin = (profit / revenue) * 100
            results.append({
                "metric": "profit_margin",
                "value": round(margin, 2),
                "formula": "Profit / Revenue"
            })

    # -----------------------------
    # ROI
    # -----------------------------
    if "investment" in text and ("gain" in text or "return" in text) and len(numbers) >= 2:
        investment, gain = numbers[0], numbers[1]
        if investment != 0:
            roi = (gain / investment) * 100
            results.append({
                "metric": "roi",
                "value": round(roi, 2),
                "formula": "Gain / Investment"
            })

    # -----------------------------
    # GROWTH
    # -----------------------------
    if "old" in text and "new" in text and len(numbers) >= 2:
        old, new = numbers[0], numbers[1]
        if old != 0:
            growth = ((new - old) / old) * 100
            results.append({
                "metric": "growth",
                "value": round(growth, 2),
                "formula": "(New - Old) / Old"
            })

    if results:
        return {"results": results}

    return {"error": "Could not understand input"}


# -----------------------------
# Routes
# -----------------------------

# Root route (for Render)
@app.get("/")
def home():
    return {"message": "Finance AI API is live 🚀"}


# Main API
@app.post("/analyze")
def analyze(request: QueryRequest):
    return smart_finance_agent(request.query)