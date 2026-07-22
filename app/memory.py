# app/memory.py

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from datetime import datetime


# =====================================================
# MEMORY STORES
# =====================================================


# Conversation memory
_store = {}


# Session metadata
_session_meta = {}


# Maximum messages sent to LLM
MAX_HISTORY_MESSAGES = 20



# =====================================================
# SESSION MANAGEMENT
# =====================================================


def get_session_history(session_id: str):

    """
    Returns chat history object.
    Creates new session if not exists.
    """

    if session_id not in _store:

        _store[session_id] = InMemoryChatMessageHistory()


        _session_meta[session_id] = {

            "created_at":
            str(datetime.now()),

            "last_activity":
            str(datetime.now()),

            "message_count":
            0,

            "investigation_context":
            {}

        }


    return _store[session_id]





def update_session_activity(session_id):

    if session_id in _session_meta:

        _session_meta[session_id][
            "last_activity"
        ] = str(datetime.now())





# =====================================================
# MESSAGE OPERATIONS
# =====================================================


def add_message(
        session_id: str,
        role: str,
        content: str
):

    """
    Store user and assistant messages.
    """


    history = get_session_history(
        session_id
    )


    if role == "user":

        history.add_message(

            HumanMessage(

                content=content

            )

        )


    elif role == "assistant":

        history.add_message(

            AIMessage(

                content=content

            )

        )


    elif role == "system":

        history.add_message(

            SystemMessage(

                content=content

            )

        )


    update_session_activity(
        session_id
    )


    _session_meta[session_id][
        "message_count"
    ] = len(history.messages)



    # Keep memory under control

    trim_history(
        session_id
    )





def trim_history(session_id):

    """
    Keep only latest messages.
    """

    history = get_session_history(
        session_id
    )


    if len(history.messages) > MAX_HISTORY_MESSAGES:

        history.messages = (

            history.messages[
                -MAX_HISTORY_MESSAGES:
            ]

        )





# =====================================================
# HISTORY ACCESS
# =====================================================


def get_history(session_id: str):

    """
    Returns recent messages for LLM.
    """


    history = get_session_history(
        session_id
    )


    trim_history(
        session_id
    )


    return history.messages





def get_message_count(session_id:str):

    return len(

        get_session_history(
            session_id
        ).messages

    )





# =====================================================
# INVESTIGATION CONTEXT
# =====================================================


def save_investigation_context(
        session_id:str,
        key:str,
        value
):

    """
    Store AML investigation information.

    Example:

    risk_score
    customer_id
    alert_id
    """

    get_session_history(
        session_id
    )


    _session_meta[session_id][
        "investigation_context"
    ][key] = value





def get_investigation_context(
        session_id:str
):

    get_session_history(
        session_id
    )


    return _session_meta[session_id].get(

        "investigation_context",

        {}

    )





# =====================================================
# SESSION INFORMATION
# =====================================================


def get_session_info(session_id:str):

    """
    Returns session details.
    """

    get_session_history(
        session_id
    )


    return _session_meta[session_id]





def list_sessions():

    """
    Admin view of active sessions.
    """

    return _session_meta





# =====================================================
# MEMORY RESET
# =====================================================


def clear_memory(
        session_id:str=None
):

    """
    Clear one session or all sessions.
    """


    global _store
    global _session_meta


    if session_id:


        _store.pop(
            session_id,
            None
        )


        _session_meta.pop(
            session_id,
            None
        )


    else:


        _store = {}

        _session_meta = {}





# =====================================================
# EXPORT CHAT
# =====================================================


def export_conversation(session_id:str):

    """
    Export conversation for audit.
    """

    history = get_history(
        session_id
    )


    return [

        {

            "role":
            message.type,

            "content":
            message.content

        }

        for message in history

    ]