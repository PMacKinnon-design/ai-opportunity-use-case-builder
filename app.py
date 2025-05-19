
import streamlit as st
import pandas as pd
import json
from utils import score_responses, analyze_uploaded_files, generate_use_case_report

st.set_page_config(page_title="AI Opportunity & Use Case Builder", layout="wide")

st.title("🤖 AI Opportunity & Use Case Builder")
st.markdown("This tool helps procurement teams identify and prioritize AI opportunities by evaluating readiness, value, and feasibility.")

st.header("📄 Upload Internal Procurement Files")
uploaded_files = st.file_uploader("Upload spend data, policies, or procedures (PDF, DOCX, CSV, TXT)", type=["pdf", "docx", "txt", "csv", "xlsx"], accept_multiple_files=True)
uploaded_data = analyze_uploaded_files(uploaded_files)

st.header("🧠 AI Opportunity Assessment Questionnaire")
with open("data/questions.json") as f:
    questions = json.load(f)

responses = {}
for q in questions:
    responses[q["id"]] = st.slider(q["question"], min_value=1, max_value=5, value=3)

if st.button("🔍 Analyze & Recommend Use Cases"):
    scores = score_responses(responses)
    use_cases_df = generate_use_case_report(scores, uploaded_data)
    st.success("AI Opportunity Report Generated")
    st.dataframe(use_cases_df)

    csv = use_cases_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Report as CSV", data=csv, file_name="ai_opportunity_report.csv", mime="text/csv")


st.header("📈 Benchmark Your AI Readiness")
st.markdown("Compare your organization's procurement AI readiness against industry leaders.")

benchmark_df = pd.read_json("data/benchmarks.json")
st.dataframe(benchmark_df)

st.bar_chart(data=benchmark_df.set_index("Function")["Industry Adoption Rate"])
