# app/memory.py

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# Store conversations by session
_store = {}


def get_session_history(session_id: str):
    """
    Returns LangChain chat history object for a session.
    """
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()

    return _store[session_id]


def add_message(session_id: str, role: str, content: str):
    """
    Add user/assistant message.
    """

    history = get_session_history(session_id)

    if role == "user":
        history.add_message(HumanMessage(content=content))
    else:
        history.add_message(AIMessage(content=content))


def clear_memory(session_id: str = None):
    """
    Clear one session or all sessions.
    """

    global _store

    if session_id:
        _store.pop(session_id, None)
    else:
        _store = {}


def get_history(session_id: str):
    """
    Returns list of LangChain messages.
    """

    return get_session_history(session_id).messages


def get_message_count(session_id: str):
    return len(get_session_history(session_id).messages)