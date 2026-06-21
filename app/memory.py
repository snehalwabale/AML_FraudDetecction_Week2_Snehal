# =====================================================
# SIMPLE CONVERSATION MEMORY
# =====================================================

conversation_history = []


def add_message(role, content):

    conversation_history.append({

        "role": role,

        "content": content
    })

    # Keep only last 10 messages

    if len(conversation_history) > 10:

        conversation_history.pop(0)


def get_history():

    history_text = ""

    for msg in conversation_history:

        history_text += (

            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    return history_text


def clear_memory():

    conversation_history.clear()


def get_message_count():

    return len(
        conversation_history
    )