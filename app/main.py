from fastapi import FastAPI

from datetime import datetime

import uuid

from app.models import (
    ChatRequest,
    HealthResponse
)

from app.memory import (
    add_message,
    get_history,
    clear_memory
)

from app.chains import (
    ask_llm
)

from app.logger import (
    log_interaction
)

app = FastAPI()

APP_START_TIME = datetime.now()


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {

        "project":
        "AML & Fraud Detection Co-Pilot",

        "status":
        "Running"
    }


# =====================================================
# HEALTH
# =====================================================

@app.get(
    "/health",
    response_model=HealthResponse
)
def health():

    uptime = datetime.now() - APP_START_TIME

    return {

        "status":
        "healthy",

        "uptime":
        str(uptime),

        "model":
        "gpt-4o-mini",

        "version":
        "1.0"
    }


# =====================================================
# RESET
# =====================================================

@app.post("/reset")
def reset():

    clear_memory()

    return {

        "success":
        True,

        "message":
        "Conversation memory cleared"
    }


# =====================================================
# CHAT
# =====================================================

@app.post("/chat")
def chat(req: ChatRequest):

    try:

        user_message = req.message

        add_message(
            "user",
            user_message
        )

        history = get_history()

        result = ask_llm(
            user_message,
            history
        )

        add_message(
            "assistant",
            result.response
        )

        session_id = str(
            uuid.uuid4()
        )

        log_interaction(

            session_id=
            session_id,

            query=
            user_message,

            response=
            result.response,

            tool_used=
            result.tool_used
        )

        return {

            "success":
            True,

            "session_id":
            session_id,

            "response":
            result.response,

            "risk_score":
            result.risk_score,

            "action":
            result.action,

            "tool_used":
            result.tool_used
        }

    except Exception as e:

        return {

            "success":
            False,

            "error":
            str(e)
        }