import pandas as pd
import requests
import argparse
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# -------------------------
# SAFE FETCHER (NO 403)
# -------------------------

def fetch_table(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return pd.read_html(r.text)[0]
    except:
        return None


# -------------------------
# INDEX SOURCES
# -------------------------

def fetch_sp500():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df = fetch_table(url)

    if df is None:
        # Fallback (never blocked)
        raw_url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
        df = pd.read_csv(raw_url)

    return df["Symbol"].tolist()


def fetch_nasdaq100():
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    df = fetch_table(url)

    if df is None:
        raw_url = "https://raw.githubusercontent.com/etomberg/nasdaq100-list/main/nasdaq100.csv"
        df = pd.read_csv(raw_url)

    return df["Symbol"].tolist()


def fetch_russell1000():
    raw_url = "https://raw.githubusercontent.com/datasets/russell-1000/master/data/russell1000.csv"
    df = pd.read_csv(raw_url)
    return df["ticker"].tolist()


# -------------------------
# GENERATOR
# -------------------------

def generate_best500(out_dir, target):
    os.makedirs(out_dir, exist_ok=True)

    print("Fetching S&P 500...")
    sp500 = fetch_sp500()

    print("Fetching Nasdaq 100...")
    nasdaq = fetch_nasdaq100()

    print("Fetching Russell 1000...")
    russell = fetch_russell1000()

    # combine
    combined = list(dict.fromkeys(sp500 + nasdaq + russell))

    # limit if needed
    final = combined[:target]

    out_path = os.path.join(out_dir, "best500.txt")
    with open(out_path, "w") as f:
        for t in final:
            f.write(t + "\n")

    print(f"Saved {len(final)} tickers → {out_path}")


# -------------------------
# CLI
# -------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=str, default="./tickers")
    parser.add_argument("--target", type=int, default=500)
    args = parser.parse_args()

    generate_best500(args.out_dir, args.target)
