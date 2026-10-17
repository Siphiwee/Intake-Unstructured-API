from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import ReviewRequest, ReviewResponse
from app.service import process_review


app = FastAPI(
    title="Structured Intake Review API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/review", response_model=ReviewResponse)
def review_request(request: ReviewRequest):
    return process_review(request)