import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AML & Fraud Detection Co-Pilot",
    layout="wide"
)

st.title("🏦 AML & Fraud Detection Co-Pilot")

st.markdown(
    """
    Analyze transactions, generate SARs,
    perform sanctions screening,
    and investigate AML alerts.
    """
)

query = st.text_input(
    "Enter AML Query"
)

col1, col2 = st.columns(2)

with col1:

    if st.button("Submit"):

        if query:

            try:

                response = requests.post(

                    f"{API_URL}/chat",

                    json={
                        "message": query
                    }
                )

                st.subheader(
                    "Response"
                )

                st.json(
                    response.json()
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

with col2:

    if st.button(
        "Reset Memory"
    ):

        try:

            response = requests.post(
                f"{API_URL}/reset"
            )

            st.success(
                "Memory Cleared"
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

st.divider()

st.subheader(
    "Quick Test Queries"
)

tests = [

    "Analyze account 55-389",

    "Generate SAR for account 55-389",

    "Screen Viktor Petrov against sanctions",

    "Is this customer a PEP?",

    "What is the AML risk score for customer C-7781?",

    "Compare transaction velocity this month vs last 6-month average",

    "Provide investigation timeline",

    "Summarize all open AML alerts"
]

for q in tests:

    st.code(q)