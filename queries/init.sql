CREATE TABLE IF NOT EXISTS futures_ohlcv (
    id SERIAL PRIMARY KEY,                      
    symbol VARCHAR(255) NOT NULL,           
    timestamp TIMESTAMP NOT NULL,             
    open DOUBLE PRECISION NOT NULL,             
    high DOUBLE PRECISION NOT NULL,             
    low DOUBLE PRECISION NOT NULL,              
    close DOUBLE PRECISION NOT NULL,           
    volume DOUBLE PRECISION NOT NULL            
)