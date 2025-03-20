import os
from datetime import datetime, timezone

import ccxt
import pandas as pd

from src.utils.loggerring import logger
from src.utils.sql_operators import (
    format_sql,
    get_query_from_sql_file,
    select,
    upload_without_duplicates,
)


def bingx_futures_date_range_1h(start_date, end_date, symbol):
    """
    Fetch historical OHLCV data for futures on BingX within a specified date range.

    Parameters
    ----------
    start_date : str
        The start date in 'YYYY-MM-DD' format.
    end_date : str
        The end date in 'YYYY-MM-DD' format.
    symbol : str
        The trading symbol (e.g., 'BTC/USDT:USDT').

    Returns
    -------
    pd.DataFrame
    """

    exchange = ccxt.bingx(
        {
            "enableRateLimit": True,
        }
    )

    start_timestamp = exchange.parse8601(start_date + "T00:00:00Z")
    today = datetime.now().strftime("%Y-%m-%d")
    if end_date == today:
        now = datetime.now(timezone.utc)
        current_hour = now.replace(minute=0, second=0, microsecond=0)
        prev_hour = current_hour.replace(hour=max(0, current_hour.hour - 1))
        end_timestamp = int(prev_hour.timestamp() * 1000)
    else:
        end_timestamp = exchange.parse8601(end_date + "T23:59:59Z")

    all_ohlcv = pd.DataFrame()

    current_timestamp = start_timestamp
    while current_timestamp < end_timestamp:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, "1h", since=current_timestamp, limit=1000)
            if not ohlcv or len(ohlcv) == 0:
                logger.warning(f"No data returned for {symbol} from {start_date} to {end_date}")
                return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
        except Exception as e:
            logger.warning(f"Error fetching data: {e}")
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

        all_ohlcv = pd.concat([all_ohlcv, df], ignore_index=True)

        current_timestamp = ohlcv[-1][0] + 3600000  # Add 1 hour in milliseconds

    all_ohlcv = all_ohlcv[
        (all_ohlcv["timestamp"] >= start_timestamp) & (all_ohlcv["timestamp"] <= end_timestamp)
    ]

    return all_ohlcv


def get_bingx_futures_ohlcv(symbol, timeframe, limit=100) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for futures on BingX.

    Parameters
    ----------
    symbol : str
        The trading symbol (e.g., 'BTC/USDT:USDT').
    timeframe : str
        The timeframe for the candles (e.g., '1h', '1d').
    limit : int, optional
        The number of candles to fetch (default is 100).

    Returns
    -------
    pd.DataFrame
    """
    # Initialize the BingX exchange
    exchange = ccxt.bingx(
        {
            "enableRateLimit": True,  # Enable rate limiting to avoid being banned
        }
    )

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

    return df


def save_ohlcv_to_csv(data, symbol, timeframe):
    """
    Fetch OHLCV data from BingX and save it as a CSV file in the `data/` directory.

    Parameters
    ----------
    data : pd.DataFrame
        The data to save.
    symbol : str
        The trading symbol (e.g., 'BTC/USDT:USDT').
    timeframe : str
        The timeframe for the candles (e.g., '1h', '1d').

    Returns
    -------
    str
        The path to the saved CSV file.
    """

    # Convert timestamp to a human-readable format
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")

    # Ensure the `data/` directory exists
    os.makedirs("data", exist_ok=True)

    # Create a filename
    filename = f"data/{symbol.replace('/', '_')}_{timeframe}_ohlcv.csv"

    # Save the DataFrame to a CSV file
    data.to_csv(filename, index=False)

    return filename


def update_futures_data(symbol, start_date, end_date):
    """
    Update the OHLCV data in PostgreSQL database for a given symbol.

    Parameters
    ----------
    symbol : str
        The trading symbol (e.g., 'BTC/USDT:USDT').
    start_date : str
        The start date in 'YYYY-MM-DD' format.
    end_date : str
        The end date in 'YYYY-MM-DD' format.
    """

    ohlcv_data = bingx_futures_date_range_1h(start_date, end_date, symbol)
    ohlcv_data["timestamp"] = pd.to_datetime(ohlcv_data["timestamp"], unit="ms")
    ohlcv_data["symbol"] = symbol
    upload_without_duplicates(ohlcv_data, table_name="futures_ohlcv")


def get_latest_futures_data(symbol):
    """
    Get the latest OHLCV data for a specific symbol.

    Parameters
    ----------
    symbol : str
        The trading symbol (e.g., 'BTC/USDT:USDT').

    Returns
    -------
    pd.DataFrame
    """
    query = get_query_from_sql_file("queries/latest_futures_data.sql")
    query = format_sql(query, params={"symbol": symbol})
    data = select(query)
    return data


if __name__ == "__main__":
    symbol = "BTC/USDT:USDT"
    start_date = "2025-03-10"
    end_date = "2025-03-19"
    timeframe = "1h"

    ohlcv_data = bingx_futures_date_range_1h(
        start_date=start_date, end_date=end_date, symbol=symbol
    )

    save_ohlcv_to_csv(ohlcv_data, symbol, timeframe)
