from fastapi import FastAPI
from app.models import ReviewRequest, ReviewResponse 
from app.service import process_review

app = FastAPI(
    title="Structured Intake Review API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/review", response_model=ReviewResponse)
def review_request(request: ReviewRequest):
    return process_review(request)

 