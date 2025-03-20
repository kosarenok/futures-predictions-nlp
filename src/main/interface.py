from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.lib.crypto_news import latest_news, update_news
from src.lib.futures_data import get_latest_futures_data, update_futures_data

st.set_page_config(page_title="Crypto Analytics Dashboard", page_icon="📊", layout="wide")


def plot_candlestick(df):
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
        title="OHLCV Chart",
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
    st.title("Crypto Analytics Dashboard")

    # Main content area
    tab1, tab2 = st.tabs(["Market Data", "Crypto News"])

    with tab1:
        st.header("Futures Market Data")
        symbol = st.selectbox("Select Symbol", ["SOL/USDT:USDT", "BTC/USDT:USDT", "ETH/USDT:USDT"])

        # Get data directly from the function instead of API
        data_df = get_latest_futures_data(symbol)
        if not data_df.empty:
            st.success(f"Data retrieved for {symbol}")
            fig = plot_candlestick(data_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No data available for {symbol}")

    with tab2:
        st.header("Latest Crypto News")
        # Get news directly from the function instead of API
        news_df = latest_news()
        if not news_df.empty:
            st.success("Latest news retrieved")
            display_news_table(news_df)
        else:
            st.warning("No news data available")

    # Footer with filters and refresh buttons
    st.markdown("---")
    st.subheader("Update Data")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        currency = st.selectbox("Select Currency for News", ["BTC", "ETH", "SOL"])

    with col2:
        # Futures data refresh section
        st.subheader("Refresh Market Data")
        futures_symbol = st.selectbox("Symbol", ["SOL/USDT:USDT", "BTC/USDT:USDT", "ETH/USDT:USDT"])

        # Date range for futures data
        today = datetime.now()
        start_default = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        end_default = today.strftime("%Y-%m-%d")

        start_date = st.date_input("Start Date", value=datetime.strptime(start_default, "%Y-%m-%d"))
        end_date = st.date_input("End Date", value=datetime.strptime(end_default, "%Y-%m-%d"))

        if st.button("Update Market Data"):
            with st.spinner("Updating market data..."):
                try:
                    update_futures_data(
                        futures_symbol,
                        start_date.strftime("%Y-%m-%d"),
                        end_date.strftime("%Y-%m-%d"),
                    )
                    st.success(f"Market data updated successfully for {futures_symbol}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update market data: {e}")

    with col3:
        # News refresh section
        st.subheader("Refresh News Data")
        st.write(f"Selected currency: {currency}")

        if st.button("Update News Data"):
            with st.spinner("Updating news data..."):
                try:
                    update_news(currency)
                    st.success(f"News data updated successfully for {currency}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update news data: {e}")


if __name__ == "__main__":
    main()
