import ccxt
import os
import pandas as pd

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
    exchange = ccxt.bingx({
        'enableRateLimit': True,  # Enable rate limiting to avoid being banned
    })

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

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
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    # Ensure the `data/` directory exists
    os.makedirs('data', exist_ok=True)

    # Create a filename
    filename = f"data/{symbol.replace('/', '_')}_{timeframe}_ohlcv.csv"

    # Save the DataFrame to a CSV file
    data.to_csv(filename, index=False)

    return filename

if __name__ == "__main__":
    symbol = 'BTC/USDT:USDT'
    timeframe = '1h'
    limit = 100

    ohlcv_data = get_bingx_futures_ohlcv(symbol, timeframe, limit)
    save_ohlcv_to_csv(ohlcv_data, symbol, timeframe)