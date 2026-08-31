from pydantic import BaseModel

Class ReviewRequest(BaseModel): 
request_text: str

Class ExtractedInformation(BaseModel):
    name: str | None =None
    request_text: str | None =None
    employment_status: str |None =None
    months_unemployed: str None =None
    address: str | None = None
    monthly_income: float | None =None


Class ValidationResult(BaseModel):
Status: str
missing_information: list[str]
invalid_information: list[str]
conflicting_information: list[str]
review_required: bool

Class ReviewResponse(BaseModel):
   extraction: ExtractedInformation
   validation: ValidationResult

