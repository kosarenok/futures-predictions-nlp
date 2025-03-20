from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.lib.futures_data import update_futures_data
from src.lib.crypto_news import update_news
from src.utils.loggerring import logger

from typing import Literal
app = FastAPI(title="Crypto Analytics API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Crypto Analytics API"}


@app.post("/api/futures/update")
async def update_futures(
    symbol: str = Query(..., description="Trading symbol (e.g., 'BTC/USDT:USDT')"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    """Update futures OHLCV data in the database."""
    try:
        update_futures_data(symbol, start_date, end_date)
        return {"status": "success", "message": f"Futures data updated for {symbol}"}
    except Exception as e:
        logger.error(f"Error updating futures data: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.post("/api/news/update")
async def update_crypto_news(
    currency: Literal["BTC", "ETH", "SOL"] = Query("BTC", description="Currency to fetch news for")
):
    """Update crypto news data in the database."""
    try:
        update_news(currency)
        return {"status": "success", "message": f"News data updated for {currency}"}
    except Exception as e:
        logger.error(f"Error updating news data: {str(e)}")
        return {"status": "error", "message": str(e)}


def start_api():
    import uvicorn

    uvicorn.run("src.main.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start_api()
