"""Allowlisted deterministic football queries; never execute user-supplied Python."""
from pathlib import Path
import pandas as pd

class ReadOnlyFootballAgent:
    def __init__(self, root=None): self.root=Path(root or Path(__file__).resolve().parent)
    def invoke(self, question):
        q=question.lower()
        if any(w in q for w in ["match", "مبار", "overview", "نظرة"]):
            frame=pd.read_csv(self.root/"matches.csv")
            return {"output":f"Distinct matches: {frame['match_id'].nunique()}. Source: matches.csv; calculation: nunique(match_id)."}
        if any(w in q for w in ["goal", "scor", "هداف"]):
            frame=pd.read_csv(self.root/"goals.csv")
            field=next((c for c in ["player_name","family_name","player_id"] if c in frame),None)
            if field is None:raise ValueError("Player field unavailable")
            values=frame.groupby(field).size().nlargest(10)
            return {"output":"Goal-event counts by "+field+" (own-goal semantics require separate review):\n"+values.to_string()+"\nSource: goals.csv; group size, not a join of multiple fact tables."}
        return {"output":"Supported read-only questions: match count/overview, or goal/scorer event counts. Arbitrary Python and unsupported questions are not executed."}
