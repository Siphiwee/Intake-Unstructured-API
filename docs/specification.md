# Structured Intake Review API

## 1. Purpose

The Structured Intake Review API receives an unstructured service request
from a user.

The API passes the request to an LLM, which extracts the required
information and returns it as structured data.

The Python application then applies deterministic validation rules to the
structured data. It identifies missing, invalid, or conflicting information
and determines whether human review is required.

The system does not make approval, rejection, or eligibility decisions.
Consequential decisions remain with a human reviewer.

## 2. User

The primary user is a reviewer who needs to assess information submitted
in an unstructured service request.

The reviewer needs to understand:

- What information was provided
- What information is missing
- What information is invalid
- What information conflicts
- Whether human review is required

## 3. API Input

The API will expose a POST endpoint:

POST /review

The request body will contain unstructured text.

Example:

{
    "request_text": "My name is John Smith. I need housing assistance. I
    have been unemployed for three months and my monthly income is R4500."
}

The API accepts the request as text and does not require the user to
provide the information in a predefined structured format.

## 4. LLM Extraction

The LLM is responsible for reading the unstructured request and extracting
specific fields into a predefined structured format.

The LLM must only extract information that is present or clearly supported
by the user's request.

The LLM must not invent, assume, or fabricate missing information.

### Required Fields

| Field | Type | Description |
|---|---|---|
| name | string or null | Name of the requester |
| request_type | string or null | Type of assistance or service requested |
| employment_status | string or null | Employment status stated by the requester |
| months_unemployed | integer or null | Number of months unemployed, if stated |
| address | string or null | Address provided by the requester |
| monthly_income | number or null | Monthly income stated by the requester |

### Example Input

"My name is John Smith. I need housing assistance. I have been unemployed
for three months and currently live at 15 Example Street. My monthly income
is R4500."

### Expected Structured Output

{
    "name": "John Smith",
    "request_type": "housing assistance",
    "employment_status": "unemployed",
    "months_unemployed": 3,
    "address": "15 Example Street",
    "monthly_income": 4500
}

### Missing Information

If a field cannot be identified from the request, the LLM should return
null for that field.

The system must not create or guess a value for a missing field.

For example:

{
    "name": "John Smith",
    "request_type": "housing assistance",
    "employment_status": "unemployed",
    "months_unemployed": 3,
    "address": null,
    "monthly_income": 4500
}


## 5. Deterministic Validation

After the LLM returns the structured extraction, the Python application
will validate the result using deterministic rules.

The validation layer is separate from the LLM.

### Required Field Validation

The following fields are required:

- name
- request_type
- employment_status
- address
- monthly_income

If a required field contains null or is otherwise missing, the validation
layer will identify it as missing information.

### Numeric Validation

The validation layer will check that:

- monthly_income is not negative
- months_unemployed is not negative

### Conflict Detection

The system should identify information that appears to contradict itself.

For example:

"I am currently unemployed, but I started working last month."

Conflicting information should result in human review rather than the
system attempting to determine which statement is correct.

### Validation Result

The validation layer should produce a clear result indicating:

- Validation status
- Missing information
- Invalid information
- Conflicting information
- Whether human review is required




## 6. Human Review Boundary

The system is designed to assist a human reviewer and must not replace the
human decision-maker.

The system must not:

- Approve a request
- Reject a request
- Determine eligibility
- Make a consequential decision on behalf of the reviewer
- Invent missing information
- Automatically treat an LLM response as correct

### Human Review Is Required When

Human review should be triggered when:

- Required information is missing
- Extracted information is invalid
- Information is contradictory
- The request is ambiguous
- The LLM produces invalid or unusable structured output
- The system detects a potentially unsafe or adversarial request

The system should clearly indicate when human attention is required.

Possible statuses include:

- READY_FOR_REVIEW
- HUMAN_REVIEW_REQUIRED
- INCOMPLETE
- INVALID
- CONFLICTING_INFORMATION

The final decision remains the responsibility of the human reviewer.



## 7. Evaluation

The system will be evaluated using a fixed synthetic evaluation dataset.

The initial evaluation set will contain at least 20 cases.

The cases will cover:

### Normal Cases

- Complete requests
- Different wording for the same information
- Requests containing additional irrelevant information
- Requests containing numerical information

### Incomplete Cases

- Missing name
- Missing address
- Missing income
- Missing employment status

### Contradictory Cases

- Conflicting employment information
- Conflicting income information
- Conflicting address information

### Ambiguous Cases

- Unclear employment status
- Unclear income
- Unclear request type

### Irrelevant Cases

- Requests unrelated to the intended use of the API
- General conversation or unrelated questions

### Adversarial Cases

- Prompt injection attempts
- Instructions attempting to override system behaviour
- Attempts to manipulate the structured output
- Malicious or irrelevant content mixed with a legitimate request

## Evaluation Metrics

The evaluation will measure:

- Field extraction accuracy
- Schema-valid output rate
- Missing-information detection
- Abstention or human-review behaviour
- Validation accuracy
- API response latency
- Failure behaviour

Evaluation results will be recorded and reviewed rather than relying only
on subjective judgement.



## 8. Data and Security Boundary

The project will use synthetic, non-identifying data only.

The following must not be used:

- Real client documents
- Production data
- Credentials
- API keys
- Confidential business rules
- Client-specific workflows
- Sensitive business information

Secrets must be stored outside source code using environment-based
configuration.

The application must avoid logging sensitive request content or secrets.

The system must treat user-provided instructions as untrusted input and
must consider prompt-injection and unsafe-output risks.

## 9. Conflict Detection and Traceability

The system must not automatically resolve contradictory information by
choosing one statement over another.

When conflicting information is detected, the system should:

1. Preserve the original unstructured request.
2. Preserve the structured extraction produced by the LLM.
3. Identify the conflicting field or information.
4. Record the conflict in the validation result.
5. Set review_required to true.
6. Route the request for human review.

The original request and extracted information should remain available so
that the reviewer can understand how the conflict was identified.

Example:

User request:

"I am currently unemployed, but I started working last month."

Possible result:

{
    "conflicting_information": [
        "Employment information is contradictory."
    ],
    "review_required": true
}

The system must not automatically determine which statement is correct.