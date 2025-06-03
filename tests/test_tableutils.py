import pandas as pd
from tableutils import pasted_text_to_df

def test_pasted_text_to_df_preserves_spaces():
    text = "Name\tDescription\nAlice Smith\tLives in New York City\nBob Jones\tWorks at Big Corp"
    df = pasted_text_to_df(text, header=0)
    assert list(df.columns) == ["Name", "Description"]
    assert df.iloc[0, 0] == "Alice Smith"
    assert df.iloc[0, 1] == "Lives in New York City"
    assert df.iloc[1, 0] == "Bob Jones"
    assert df.iloc[1, 1] == "Works at Big Corp"
