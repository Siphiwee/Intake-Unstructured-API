from app.models import ReviewRequest
from app.extractor import extract_information
from app.validation import validate_information


def process_review(request: ReviewRequest):
    extracted_data = extract_information(request.request_text)

    validation_result = validate_information(extracted_data)

    return {
        "message": "Request processed",
        "extraction": extracted_data,
        "validation": validation_result
    }