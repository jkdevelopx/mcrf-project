from utils.load_universe import load_universe
from engine import scan_universe, add_scores

def run_scanner():
    universe = load_universe(include="all")  # ← ใช้ S&P500 + Nasdaq100 + Russell1000
    print(f"Universe loaded: {len(universe)} tickers")

    df = scan_universe(universe)
    df = add_scores(df)
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    return df
