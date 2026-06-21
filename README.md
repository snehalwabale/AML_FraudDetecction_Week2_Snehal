# AML & Fraud Detection Co-Pilot

## Overview

AI-powered AML investigation assistant built using:

- LangChain
- OpenAI
- FastAPI
- Streamlit
- Pydantic
- Structured Logging

## Features

### Transaction Pattern Analyzer

Detects:

- Structuring
- Layering
- Rapid Movement
- Round Tripping

### SAR Generator

Generates Suspicious Activity Reports.

### Sanctions & PEP Screening

Checks:

- OFAC
- UN
- EU
- PEP Databases

## API Endpoints

### Health

GET /health

### Chat

POST /chat

### Reset

POST /reset

## Run Backend

uvicorn app.main:app --reload

## Run Frontend

streamlit run frontend/streamlit_app.py

## Testing

pytest