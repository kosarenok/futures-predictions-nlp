SELECT
    symbol,
    timestamp,
    open,
    high,
    low,
    close,
    volume
FROM futures_ohlcv
WHERE symbol = {symbol}
ORDER BY timestamp DESC