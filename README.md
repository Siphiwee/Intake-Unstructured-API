# Structured Intake Review API

## Overview

The Structured Intake Review API is an AI-powered service that converts unstructured service-request text into structured information and applies deterministic validation rules to identify cases that are ready for processing or require human review.

The project demonstrates how an LLM can be incorporated into a reliable application architecture without allowing the LLM to make the final business decision.

The core principle is:

> **The LLM interprets, Python validates, and the human decides.**

---

## Problem Statement

Service-request information is often provided as unstructured text. Important information may be missing, invalid, conflicting, or contain potentially adversarial instructions.

The purpose of this application is to:

1. Accept unstructured service-request text.
2. Extract relevant information using an LLM.
3. Return the extracted information in a structured format.
4. Apply deterministic Python validation rules.
5. Identify missing, invalid, conflicting, or potentially unsafe information.
6. Route problematic cases for human review.
7. Provide an evaluation framework to measure system behaviour.

The system does **not** make approval or eligibility decisions.

---

## Solution

The application separates LLM interpretation from deterministic validation.

```text
Client
   |
   v
FastAPI
   |
   v
Service Layer
   |
   v
LLM Extraction
   |
   v
Structured Pydantic Model
   |
   v
Deterministic Validation
   |
   +----------------------------+
   |                            |
   v                            v
READY_FOR_PROCESSING     HUMAN_REVIEW_REQUIRED