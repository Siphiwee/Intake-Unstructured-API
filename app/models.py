from pydantic import BaseModel


class ReviewRequest(BaseModel):
    request_text: str


class ExtractedInformation(BaseModel):
    name: str | None = None
    request_text: str | None = None
    employment_status: str | None = None
    months_unemployed: int | None = None
    address: list[str] | None = None
    monthly_income: float | None = None


class ValidationResult(BaseModel):
    status: str
    missing_information: list[str]
    invalid_information: list[str]
    conflicting_information: list[str]
    review_required: bool
    review_reasons: list[str]


class ReviewResponse(BaseModel):
    message: str
    extraction: ExtractedInformation
    validation: ValidationResult



