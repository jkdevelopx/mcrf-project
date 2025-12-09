# ai_agent.py
import os
import openai
from run_scanner import run_scan
import pandas as pd

openai_api_key = os.environ.get("OPENAI_API_KEY")
if openai_api_key:
    openai.api_key = openai_api_key

def summarize_picks(df_top: pd.DataFrame):
    if openai_api_key is None:
        return "OpenAI key not set. Install OPENAI_API_KEY to enable AI summaries."
    text = df_top.head(7).to_string(index=False)
    prompt = f"Summarize these stock picks into 3 concise bullet points with risks and reasons:\n\n{text}"
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # change if needed
        messages=[{"role":"user","content":prompt}],
        max_tokens=250
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    uni = pd.read_csv("data/universe_small.csv")['ticker'].astype(str).tolist()
    top = run_scan(uni)
    print(top)
    print(summarize_picks(top))
