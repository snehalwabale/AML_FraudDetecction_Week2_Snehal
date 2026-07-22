import json
from pathlib import Path

import streamlit as st

REPORT_DIR = Path("reports")


st.title("AML Evaluation Dashboard")

reports = sorted(

    REPORT_DIR.glob("*.json"),

    reverse=True

)

if not reports:

    st.warning(

        "No evaluation reports found."

    )

    st.stop()

selected = st.selectbox(

    "Select Report",

    reports

)

with open(

    selected,

    "r",

    encoding="utf-8"

) as f:

    report = json.load(f)

summary = report["summary"]

st.metric(

    "Pass Rate",

    f"{summary['pass_rate'] * 100:.2f}%"

)

st.metric(

    "Total Questions",

    summary["total"]

)

st.metric(

    "Passed",

    summary["passed"]

)

st.subheader("Detailed Results")

st.json(

    report["results"]

)