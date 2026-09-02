from app.models import ExtractedInformation


def extract_information(request_text: str) -> ExtractedInformation:
    return ExtractedInformation(
        name="John",
        request_text=request_text,
        employment_status="unemployed",
        months_unemployed=6,
        address="Durban",
        monthly_income=None
    )