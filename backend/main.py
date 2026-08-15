from datetime import datetime, time
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Expense Anomaly Demo API")

# Enable CORS so the local frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    merchant: str
    amount: float
    timestamp: datetime

class TransactionAnalysisResult(BaseModel):
    merchant: str
    amount: float
    timestamp: datetime
    risk_score: int
    flagged: bool

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "expense-anomaly-backend"}

@app.post("/analyze", response_model=List[TransactionAnalysisResult])
def analyze_transactions(transactions: List[Transaction]):
    if not transactions:
        return []

    # Calculate the average amount of the transaction batch
    total_amount = sum(t.amount for t in transactions)
    avg_amount = total_amount / len(transactions)

    # Count merchant frequencies to check for single occurrences
    merchant_counts = {}
    for t in transactions:
        merchant_counts[t.merchant] = merchant_counts.get(t.merchant, 0) + 1

    results = []
    for t in transactions:
        score = 0

        # Rule 1: amount above 3x the average gets +40
        if t.amount > 3 * avg_amount:
            score += 40

        # Rule 2: transaction time between 00:00 and 05:00 gets +30
        tx_time = t.timestamp.time()
        if time(0, 0) <= tx_time <= time(5, 0):
            score += 30

        # Rule 3: merchant appearing only once in the batch gets +30
        if merchant_counts[t.merchant] == 1:
            score += 30

        # Ensure risk score is capped between 0 and 100
        score = min(max(score, 0), 100)
        flagged = score >= 50

        results.append(
            TransactionAnalysisResult(
                merchant=t.merchant,
                amount=t.amount,
                timestamp=t.timestamp,
                risk_score=score,
                flagged=flagged
            )
        )

    return results

