import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "tickers")

def load_list(filename: str) -> list:
    path = os.path.join(BASE_DIR, filename)
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_universe(include="all"):
    """
    include: "sp500", "nasdaq100", "r1000", "all"
    """
    tickers = []

    if include in ("sp500", "all"):
        tickers += load_list("sp500.txt")

    if include in ("nasdaq100", "all"):
        tickers += load_list("nasdaq100.txt")

    if include in ("r1000", "all"):
        tickers += load_list("russell1000.txt")

    # remove duplicates
    tickers = list(sorted(set(tickers)))
    return tickers
