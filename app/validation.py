from app.models import ExtractedInformation, ValidationResult


def validate_information(data: ExtractedInformation) -> ValidationResult:

    missing_information = []
    invalid_information = []
    conflicting_information = []

    # Required information
    if data.name is None:
        missing_information.append("name")

    if data.address is None:
        missing_information.append("address")

    if data.monthly_income is None:
        missing_information.append("monthly_income")

    # Invalid information
    if data.monthly_income is not None and data.monthly_income < 0:
        invalid_information.append("monthly_income")

    if data.months_unemployed is not None and data.months_unemployed < 0:
        invalid_information.append("months_unemployed")

    # Determine whether human review is required
    review_required = (
        len(missing_information) > 0
        or len(invalid_information) > 0
        or len(conflicting_information) > 0
    )

    if review_required:
        status = "HUMAN_REVIEW_REQUIRED"
    else:
        status = "READY_FOR_PROCESSING"

    return ValidationResult(
        status=status,
        missing_information=missing_information,
        invalid_information=invalid_information,
        conflicting_information=conflicting_information,
        review_required=review_required
    )