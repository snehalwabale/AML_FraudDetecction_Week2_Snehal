import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(

    page_title="AML & Fraud Detection Co-Pilot",

    page_icon="🏦",

    layout="wide"

)

if "messages" not in st.session_state:

    st.session_state.messages = []

if "session_id" not in st.session_state:

    import uuid

    st.session_state.session_id = str(uuid.uuid4())

st.title("🏦 AML & Fraud Detection Co-Pilot")

st.caption("AI-powered Investigation Assistant")

with st.sidebar:

    st.header("System")

    if st.button("Health Check"):

        try:

            response = requests.get(

                f"{FASTAPI_URL}/health"

            )

            st.success(response.json()["status"])

        except:

            st.error("Backend not running")

    if st.button("Clear Conversation"):

        try:

            requests.post(

                f"{FASTAPI_URL}/reset",

                params={

                    "session_id":

                    st.session_state.session_id

                }

            )

        except:

            pass

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.write(

        "Model : GPT-4o Mini"

    )

    st.write(

        "Backend : FastAPI"

    )

    st.write(

        "Memory : LangChain"

    )

    st.write(

        "RAG : FAISS"

    )

for message in st.session_state.messages:

    with st.chat_message(

        message["role"]

    ):

        st.markdown(

            message["content"]

        )

prompt = st.chat_input(

    "Ask an AML investigation question..."

)

if prompt:

    st.session_state.messages.append(

        {

            "role": "user",

            "content": prompt

        }

    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Investigating..."):

            try:

                response = requests.post(

                    f"{FASTAPI_URL}/chat",

                    json={

                        "message": prompt,

                        "session_id": st.session_state.session_id

                    }

                )

                result = response.json()

                answer = result.get(

                    "response",

                    "No response received."

                )

                st.markdown(answer)

                if result.get("citations"):

                    with st.expander(

                        "Retrieved Sources"

                    ):

                        for citation in result["citations"]:

                            st.markdown(

                                f"**Document:** {citation.get('doc_id','Unknown')}"

                            )

                            st.write(

                                citation.get(

                                    "chunk_text",

                                    ""

                                )[:300]

                            )

                            st.markdown("---")

                st.session_state.messages.append(

                    {

                        "role": "assistant",

                        "content": answer

                    }

                )

            except Exception as e:

                error = f"Error : {e}"

                st.error(error)

                st.session_state.messages.append(

                    {

                        "role": "assistant",

                        "content": error

                    }

                )