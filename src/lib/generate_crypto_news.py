from typing import Literal

import pandas as pd
import requests

from config.variables import CRYPTO_PANIC_BASE_URL


def get_latest_crypto_news(currency: Literal["BTC", "ETH", "SOL"], page_number: int = 1) -> dict:
    """
    Fetch the latest crypto news from CryptoPanic.
    Default currencies are BTC, ETH, and SOL.

    Parameters
    ----------
    page_number : int, optional
        The page number to fetch (default is 1).

    currency : Literal['BTC', 'ETH', 'SOL']
        Currency to fetch (default is 'BTC').

    Returns
    -------
    dict
        The latest news.
    """
    fetch_url = f"{CRYPTO_PANIC_BASE_URL}&currencies={currency}&page={page_number}"
    response = requests.get(fetch_url)
    response.raise_for_status()

    return response.json()


def process_news(news_data: dict) -> pd.DataFrame:
    """
    Process crypto news data from API response and convert to a pandas DataFrame.

    Parameters
    ----------
    news_data : dict
        The JSON response from the CryptoPanic API.

    Returns
    -------
    pd.DataFrame
        DataFrame with news details including title, published date, URL, and various vote metrics.
    """
    results = news_data.get("results", [])

    data = []
    for item in results:
        votes = item.get("votes", {})

        row = {
            "id": item.get("id", ""),
            "title": item.get("title", ""),
            "published_at": item.get("published_at", ""),
            "url": item.get("url", ""),
            "negative": votes.get("negative", 0),
            "positive": votes.get("positive", 0),
            "important": votes.get("important", 0),
            "liked": votes.get("liked", 0),
            "disliked": votes.get("disliked", 0),
            "lol": votes.get("lol", 0),
            "toxic": votes.get("toxic", 0),
            "saved": votes.get("saved", 0),
            "comments": votes.get("comments", 0),
        }
        data.append(row)

        df = pd.DataFrame(data)

        # Convert published_at to datetime and then to Unix timestamp
        df["published_at"] = pd.to_datetime(df["published_at"])
        df["published_at"] = df["published_at"].astype("int64") // 10**9

    return df
