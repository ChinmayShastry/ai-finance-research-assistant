import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

from config import SENTIMENT_PERIODS
from data.nifty250 import NIFTY_250_STOCKS, STOCK_SECTORS
from data.commodities import COMMODITIES
from modules.market_data import get_price_summary, get_usd_inr_rate
from modules.news_fetcher import get_news_for_asset, filter_news_by_period
from modules.sentiment_analyzer import analyze_sentiment_for_period, generate_sentiment_report
from modules.report_generator import generate_long_term_report, generate_upcoming_factors_report
from modules.utils import format_market_cap, create_price_chart, create_volume_chart, color_change

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if "openai_key" not in st.session_state:
    st.session_state.openai_key = OPENAI_API_KEY

if "news_key" not in st.session_state:
    st.session_state.news_key = NEWS_API_KEY

@st.cache_data(ttl=900)
def cached_price_summary(ticker, is_commodity):
    return get_price_summary(ticker, is_commodity)

@st.cache_data(ttl=3600)
def cached_news(asset):
    return get_news_for_asset(asset, days=90)

# --- Page Config ---
st.set_page_config(
    page_title="AI Financial Research Assistant",
    page_icon="📊",
    layout="wide",
)

# --- Header ---
st.title("📊 AI Financial Research Assistant")
st.caption("Indian Markets | Nifty 250 Stocks & Major Commodities | Powered by OpenAI")
st.divider()

# --- Sidebar ---
with st.sidebar:

    st.header("⚙️ Configuration")

    with st.expander("🔐 API Keys", expanded=True):

        st.caption(
            "Your API keys are stored only for the current session and are never saved."
        )

        # OpenAI Key

        if not st.session_state.openai_key:

            user_openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Enter your OpenAI API Key"
            )

            if user_openai_key:
                st.session_state.openai_key = user_openai_key

        # NewsAPI Key

        if not st.session_state.news_key:

            user_news_key = st.text_input(
                "NewsAPI Key (Optional)",
                type="password",
                help="Enter your NewsAPI Key"
            )

            if user_news_key:
                st.session_state.news_key = user_news_key

    api_status = (
        "✅ Available"
        if st.session_state.openai_key
        else "❌ Required"
    )

    news_status = (
        "✅ Available"
        if st.session_state.news_key
        else "⚠️ Optional (Google RSS Only)"
    )

    st.markdown(f"OpenAI API: {api_status}")
    st.markdown(f"NewsAPI: {news_status}")

    st.divider()
    st.header("🔍 Select Asset")

    asset_type = st.radio("Asset Type", ["Stocks", "Commodities"])

    if asset_type == "Stocks":
        sector_filter = st.selectbox(
            "Filter by Sector (optional)",
            ["All Sectors"] + list(STOCK_SECTORS.keys()),
        )

        if sector_filter == "All Sectors":
            stock_options = sorted(NIFTY_250_STOCKS.keys())
        else:
            stock_options = sorted(STOCK_SECTORS.get(sector_filter, []))

        selected_asset = st.selectbox(
            "Select Stock",
            stock_options,
            index=0,
        )
        selected_ticker = NIFTY_250_STOCKS.get(selected_asset, "")
        is_commodity = False
    else:
        selected_asset = st.selectbox(
            "Select Commodity",
            sorted(COMMODITIES.keys()),
        )
        selected_ticker = COMMODITIES.get(selected_asset, "")
        is_commodity = True

    st.divider()
    analyze_button = st.button("🚀 Generate Analysis", type="primary", use_container_width=True)

# --- Main Content ---
if not st.session_state.openai_key:

    st.warning(
        "Please enter an OpenAI API Key in the sidebar to generate AI-powered reports."
    )

    st.stop()

if analyze_button and selected_asset:
    st.subheader(f"Analysis: {selected_asset}")

    # --- Price Data ---
    with st.spinner("Fetching market data..."):
        price_data = cached_price_summary(selected_ticker, is_commodity=is_commodity)

    if "error" in price_data:
        st.error(f"Could not fetch data for {selected_asset}. Please try again.")
        st.stop()

    # --- Display Price Metrics ---
    st.markdown("### 📈 Price Overview")
    price_changes = price_data.get("price_changes", {})
    info = price_data.get("info", {})

    
    if info:

        if is_commodity:
    
            col1, col2, col3, col4 = st.columns(4)
    
            with col1:
                st.metric(
                    "Current Price",
                    f"₹{info.get('current_price', 'N/A')}"
                )
    
            with col2:
                st.metric(
                    "USD/INR Rate",
                    round(price_data.get("usd_inr_rate", 0), 2)
                    if price_data.get("usd_inr_rate")
                    else "N/A"
                )
    
            with col3:
                st.metric(
                    "52W High",
                    f"₹{info.get('52w_high', 'N/A')}"
                )
    
            with col4:
                st.metric(
                    "52W Low",
                    f"₹{info.get('52w_low', 'N/A')}"
                )
    
            st.caption(
                "Commodity prices represent global futures contracts converted to INR using the current USD/INR exchange rate. These are not MCX or Indian spot market prices."
            )
        else:
    
            col1, col2, col3, col4 = st.columns(4)
    
            with col1:
                st.metric(
                    "Current Price",
                    f"₹{info.get('current_price', 'N/A')}"
                )
    
            with col2:
                sector = info.get("sector") or "N/A"
    
                st.metric(
                    "Sector",
                    sector
                )
    
            with col3:
                market_cap = info.get("market_cap", 0)
    
                st.metric(
                    "Market Cap",
                    format_market_cap(market_cap)
                    if market_cap
                    else "N/A"
                )
    
            with col4:
                pe_ratio = info.get("pe_ratio")
    
                st.metric(
                    "P/E Ratio",
                    pe_ratio if pe_ratio not in [None, "", "N/A"] else "N/A"
                )

    if price_changes:
        cols = st.columns(4)
        for i, (period, data) in enumerate(price_changes.items()):
            with cols[i]:
                st.metric(
                    f"{period} Change",
                    f"₹{data['current']}",
                    delta=f"{data['change_pct']:+.2f}%",
                )

    # --- Price Chart ---
    df = price_data.get("dataframe", pd.DataFrame())
    if not df.empty:
        fig = create_price_chart(df, f"{selected_asset} - Price Chart (3 Months)")
        st.plotly_chart(fig, use_container_width=True)

        vol_fig = create_volume_chart(df, f"{selected_asset} - Volume")
        st.plotly_chart(vol_fig, use_container_width=True)

    st.divider()

    # --- News Fetching ---
    with st.spinner("Fetching news articles..."):
        all_articles = cached_news(selected_asset)

    st.markdown(f"*Found {len(all_articles)} news articles*")

    # --- Sentiment Report ---
    st.markdown("### 🧠 Sentiment Report")
    st.caption("What the market is thinking about this asset")

    period_sentiments = {}
    progress_bar = st.progress(0)

    for i, (period_label, days) in enumerate(SENTIMENT_PERIODS.items()):
        with st.spinner(f"Analyzing sentiment for {period_label}..."):
            period_articles = filter_news_by_period(all_articles, days)
            sentiment = analyze_sentiment_for_period(
                selected_asset, period_articles, period_label
            )
            period_sentiments[period_label] = sentiment
        progress_bar.progress((i + 1) / len(SENTIMENT_PERIODS))

    progress_bar.empty()
    
    for period, sentiment in period_sentiments.items():
        with st.expander(f"📅 {period}", expanded=(period == "7 Days")):
            st.write(sentiment)

    st.divider()

    # --- Long Term Report ---
    st.markdown("### 📋 Long-Term Analysis Report")
    st.caption("Price changes, trends, and probable reasons")

    with st.spinner("Generating long-term analysis..."):
        long_term_report = generate_long_term_report(
            asset_name=selected_asset,
            price_changes=price_changes,
            articles=all_articles,
            stock_info=info,
        )

    st.write(long_term_report)

    st.divider()

    # --- Upcoming Factors ---
    st.markdown("### 🔮 Upcoming Factors")
    st.caption("Events and catalysts that could affect the price")

    with st.spinner("Identifying upcoming factors..."):
        upcoming_report = generate_upcoming_factors_report(
            asset_name=selected_asset,
            articles=all_articles,
            stock_info=info,
        )
    with st.expander("🔐 API Keys"):

    st.caption(
        "Your API keys are stored only for the current session and are never saved."
    )

    st.write(upcoming_report)

    st.divider()

    # --- Recent News ---
    st.markdown("### 📰 Recent News Headlines")
    for article in all_articles[:10]:
        st.markdown(
            f"- **{article['title']}** — *{article.get('source', '')}* ({article.get('published_at', '')[:10]})"
        )

elif not analyze_button:
    st.info("👈 Select an asset from the sidebar and click **Generate Analysis** to start.")

    st.markdown("### What this tool provides:")
    st.markdown("""
    1. **Sentiment Report** — What traders/investors are thinking (5D, 15D, 30D, 3M)
    2. **Long-Term Analysis** — Price changes, trends, and probable reasons
    3. **Upcoming Factors** — Events and catalysts that could affect prices

    ---
    **Coverage:**
    - 📊 Nifty 250 Stocks (NSE)
    - 🏗️ Major MCX Commodities (Gold, Silver, Crude Oil, Natural Gas, Copper, Zinc, Aluminium, Nickel, Cotton, Mentha Oil)
    """)
