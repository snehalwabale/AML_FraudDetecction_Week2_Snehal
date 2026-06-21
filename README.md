# AML & Fraud Detection Co-Pilot

## Overview

AI-powered AML investigation assistant built using:

- LangChain
- OpenAI
- FastAPI
- Streamlit
- Pydantic
- Structured Logging



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