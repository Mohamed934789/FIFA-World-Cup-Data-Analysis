"""Local read-only query UI, deliberately not an unrestricted dataframe agent."""
import streamlit as st
from analysis_tools import ReadOnlyFootballAgent
st.set_page_config(page_title="Football Data Explorer")
st.title("Football Data Explorer")
st.caption("Deterministic allowlisted queries; no LLM, API key, paid call or Python execution tool.")
question=st.text_input("Ask about match counts or goal/scorer event counts")
if st.button("Query") and question.strip():
    try:st.text(ReadOnlyFootballAgent().invoke(question)["output"])
    except (ValueError,KeyError,FileNotFoundError):st.error("Required dataset columns or files are unavailable.")
