CREATE TABLE IF NOT EXISTS futures_ohlcv (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL
);

CREATE INDEX idx_futures_ohlcv_symbol ON futures_ohlcv(symbol);
CREATE INDEX idx_futures_ohlcv_timestamp ON futures_ohlcv(timestamp);
CREATE INDEX idx_futures_ohlcv_symbol_timestamp ON futures_ohlcv(symbol, timestamp);

COMMENT ON TABLE futures_ohlcv IS 'Stores cryptocurrency futures OHLCV (Open, High, Low, Close, Volume) time series data';

CREATE TABLE IF NOT EXISTS crypto_news (
    id BIGINT PRIMARY KEY,
    title TEXT NOT NULL,
    published_at BIGINT NOT NULL,  -- Unix timestamp
    url TEXT NOT NULL,
    negative INTEGER NOT NULL DEFAULT 0,
    positive INTEGER NOT NULL DEFAULT 0,
    important INTEGER NOT NULL DEFAULT 0,
    liked INTEGER NOT NULL DEFAULT 0,
    disliked INTEGER NOT NULL DEFAULT 0,
    lol INTEGER NOT NULL DEFAULT 0,
    toxic INTEGER NOT NULL DEFAULT 0,
    saved INTEGER NOT NULL DEFAULT 0,
    comments INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crypto_news_published_at ON crypto_news(published_at);
CREATE INDEX idx_crypto_news_title ON crypto_news(title);
COMMENT ON TABLE crypto_news IS 'Stores cryptocurrency news articles with engagement metrics from CryptoPanic API';
