# FIFA World Cup Data Analysis

Supporting Python/Power BI learning project using the committed CSVs, `Dashboard.pbix` and presentation.
Python 3.12: install `requirements.txt`, Run All in `World_Cup.ipynb`, or run
`python -m streamlit run chatbot.py`. The optional UI is now an allowlisted deterministic data explorer:
it supports match totals and goal-event counts, rejects unsupported requests, uses no API key and
does not execute user-supplied Python. This deliberately removes the unsafe unrestricted dataframe agent;
it is not advertised as a general AI chatbot.

The notebook profiles each fact table at its own grain and avoids multiplicative joins. Goal-event
counts are not automatically equivalent to official top-scorer totals (own goals need careful treatment).
Existing BI assets remain; Desktop refresh, measures and historical coverage need separate verification.
Run `python -m pytest -q` after installing `requirements-dev.txt` for offline query checks.
