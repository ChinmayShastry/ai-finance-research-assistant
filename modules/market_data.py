import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_stock_data(ticker: str, period_days: int = 90) -> pd.DataFrame:
    """Fetch historical stock data from Yahoo Finance."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)

    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))

    if df.empty:
        return pd.DataFrame()

    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df


def get_stock_info(ticker: str) -> dict:
    """Fetch basic stock info (name, sector, market cap, etc.)."""
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        return {
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "currency": info.get("currency", "INR"),
        }
    except Exception:
        return {}


def get_commodity_data(ticker: str, period_days: int = 90) -> pd.DataFrame:
    """Fetch historical commodity data."""
    return get_stock_data(ticker, period_days)


def get_usd_inr_rate() -> float:
    """Get current USD/INR exchange rate for commodity price conversion."""
    try:
        fx = yf.Ticker("USDINR=X")
        rate = fx.info.get("regularMarketPrice", 83.0)
        return rate
    except Exception:
        return 83.0


def calculate_price_changes(df: pd.DataFrame) -> dict:
    """Calculate price changes for different periods."""
    if df.empty or len(df) < 2:
        return {}

    current_price = df["Close"].iloc[-1]
    changes = {}

    periods = {"5D": 5, "15D": 15, "30D": 30, "3M": 90}
    for label, days in periods.items():
        if len(df) >= days:
            past_price = df["Close"].iloc[-days]
        else:
            past_price = df["Close"].iloc[0]

        change_pct = ((current_price - past_price) / past_price) * 100
        changes[label] = {
            "current": round(current_price, 2),
            "past": round(past_price, 2),
            "change_pct": round(change_pct, 2),
        }

    return changes


def get_price_summary(ticker: str, is_commodity: bool = False) -> dict:
    """Get a complete price summary for a ticker."""
    df = get_stock_data(ticker, period_days=100)
    if df.empty:
        return {"error": "No data available"}

    price_changes = calculate_price_changes(df)
    info = get_stock_info(ticker) if not is_commodity else {}

    usd_inr = None
    if is_commodity and info.get("currency") == "USD":
        usd_inr = get_usd_inr_rate()

    return {
        "info": info,
        "price_changes": price_changes,
        "dataframe": df,
        "usd_inr_rate": usd_inr,
    }
