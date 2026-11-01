from analysis_tools import ReadOnlyFootballAgent
def test_queries_are_read_only_and_unsupported_code_is_not_executed(tmp_path):
    (tmp_path/"matches.csv").write_text("match_id\na\na\nb\n")
    tool=ReadOnlyFootballAgent(tmp_path)
    assert "Distinct matches: 2" in tool.invoke("match count")["output"]
    assert "not executed" in tool.invoke("import os; delete everything")["output"]
