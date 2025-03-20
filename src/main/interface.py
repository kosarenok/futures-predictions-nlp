from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.lib.crypto_news import latest_news, update_news
from src.lib.futures_data import get_latest_futures_data, update_futures_data

st.set_page_config(page_title="Crypto Analytics Dashboard", page_icon="📊", layout="wide")


def plot_candlestick(df, symbol):
    """Create a candlestick chart from OHLCV data."""
    if df.empty:
        st.warning("No data available for plotting")
        return None

    # Convert timestamp to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["timestamp"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                increasing_line_color="green",
                decreasing_line_color="red",
            )
        ]
    )

    fig.update_layout(
        title=f"OHLCV {symbol} Data",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        height=600,
    )

    return fig


def display_news_table(news_df):
    """Display news items in a formatted table."""
    if news_df.empty:
        st.warning("No news data available")
        return

    # Display only relevant columns
    if (
        "published_at" in news_df.columns
        and "title" in news_df.columns
        and "url" in news_df.columns
    ):
        display_df = news_df[["published_at", "title", "url"]].copy()

        # Convert timestamp to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(display_df["published_at"]):
            display_df["published_at"] = pd.to_datetime(display_df["published_at"], unit="s")

        # Format the published_at column
        display_df["published_at"] = display_df["published_at"].dt.strftime("%Y-%m-%d %H:%M")

        # Make titles clickable with hyperlinks
        display_df["title"] = display_df.apply(
            lambda row: f"<a href='{row['url']}' target='_blank'>{row['title']}</a>", axis=1
        )

        # Drop the URL column as it's now embedded in the title
        display_df = display_df[["published_at", "title"]]

        # Rename columns for display
        display_df.columns = ["Published At", "Title"]

        # Display the table with HTML
        st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.warning("News data has unexpected format")


def main():
    st.title("Crypto News Prediction Interface")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Choose symbol")
        user_symbol = st.selectbox("Select Symbol", ["SOL", "BTC", "ETH"])
        futures_symbol = f"{user_symbol}/USDT:USDT"

    with col2:
        # Futures data refresh section
        st.subheader("Choose date")

        # Date range for futures data
        today = datetime.now()
        start_default = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        end_default = (today - timedelta(days=1)).strftime("%Y-%m-%d")

        start_date = st.date_input("Start Date", value=datetime.strptime(start_default, "%Y-%m-%d"))
        end_date = st.date_input("End Date", value=datetime.strptime(end_default, "%Y-%m-%d"))

    if st.button("Refresh Data"):
        with st.spinner("Updating market data..."):
            try:
                update_futures_data(
                    futures_symbol,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                )
                update_news(user_symbol)
                st.success(f"Market data updated successfully for {futures_symbol}")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to update market data: {e}")

    st.markdown("---")

    st.header("Futures Market Data")

    # Get data directly from the function instead of API
    data_df = get_latest_futures_data(futures_symbol)
    if not data_df.empty:
        st.success(f"Data retrieved for {futures_symbol}")
        fig = plot_candlestick(data_df, futures_symbol)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        update_futures_data(
            futures_symbol,
            start_date=(today - timedelta(days=10)).strftime("%Y-%m-%d"),
            end_date=(today - timedelta(days=1)).strftime("%Y-%m-%d"),
        )

    st.markdown("---")

    st.header("Latest Crypto News")
    news_df = latest_news()
    if not news_df.empty:
        st.success("Latest news retrieved")
        display_news_table(news_df)
    else:
        update_news(user_symbol)


if __name__ == "__main__":
    main()
