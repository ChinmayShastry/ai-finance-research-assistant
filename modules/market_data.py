import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from yfinance.exceptions import YFRateLimitError


def get_stock_data(ticker: str, period_days: int = 90):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)

    try:

        stock = yf.Ticker(ticker)

        df = stock.history(
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d")
        )

        if df.empty:
            print(f"Empty DataFrame: {ticker}")
            return pd.DataFrame()

        df = df.reset_index()

        df = df.dropna(subset=["Close"])

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

        print(f"\nTicker: {ticker}")
        print(df[["Date", "Close"]].tail())
        return df

    except YFRateLimitError:

        print(f"Yahoo Rate Limited: {ticker}")
        return pd.DataFrame()

    except Exception as e:

        print(f"Yahoo Error ({ticker}): {e}")
        return pd.DataFrame()


def get_stock_info(ticker: str) -> dict:

    try:

        stock = yf.Ticker(ticker)

        try:
            info = stock.info
        except Exception:
            info = {}

        try:
            fast = stock.fast_info
        except Exception:
            fast = {}

        return {
            "name":
                info.get("longName")
                or ticker.replace(".NS", ""),

            "sector":
                info.get("sector")
                or "N/A",

            "industry":
                info.get("industry")
                or "N/A",

            "market_cap":
                info.get("marketCap")
                or fast.get("marketCap")
                or 0,

            "pe_ratio":
                info.get("trailingPE")
                or "N/A",

            "52w_high":
                info.get("fiftyTwoWeekHigh")
                or fast.get("yearHigh")
                or "N/A",

            "52w_low":
                info.get("fiftyTwoWeekLow")
                or fast.get("yearLow")
                or "N/A",

            "current_price":
                fast.get("lastPrice")
                or info.get("currentPrice")
                or info.get("regularMarketPrice")
                or "N/A",

            "currency":
                info.get("currency")
                or fast.get("currency")
                or "INR",
        }

    except YFRateLimitError:

        print(f"Yahoo Info Rate Limited: {ticker}")

        return {
            "name": ticker.replace(".NS", ""),
            "sector": "N/A",
            "industry": "N/A",
            "market_cap": 0,
            "pe_ratio": "N/A",
            "52w_high": "N/A",
            "52w_low": "N/A",
            "current_price": "N/A",
            "currency": "INR",
        }

    except Exception as e:

        print(f"Stock Info Error ({ticker}): {e}")

        return {
            "name": ticker.replace(".NS", ""),
            "sector": "N/A",
            "industry": "N/A",
            "market_cap": 0,
            "pe_ratio": "N/A",
            "52w_high": "N/A",
            "52w_low": "N/A",
            "current_price": "N/A",
            "currency": "INR",
        }


def get_commodity_data(ticker: str, period_days: int = 90):
    return get_stock_data(ticker, period_days)


def get_usd_inr_rate() -> float:

    try:

        fx = yf.Ticker("USDINR=X")

        try:
            return (
                fx.fast_info.get("lastPrice")
                or fx.info.get("regularMarketPrice")
                or 83.0
            )

        except Exception:
            return 83.0

    except Exception:
        return 83.0


def calculate_price_changes(df: pd.DataFrame) -> dict:

    if df.empty or len(df) < 2:
        return {}

    df = df.dropna(subset=["Close"])

    if df.empty:
        return {}

    current_price = float(df["Close"].iloc[-1])

    changes = {}

    periods = {
        "7D": 7,
        "30D": 30,
        "90D": 90,
    }

    for label, days in periods.items():

        if len(df) >= days:
            past_price = float(df["Close"].iloc[-days])
        else:
            past_price = float(df["Close"].iloc[0])

        change_pct = ((current_price - past_price) / past_price) * 100

        changes[label] = {
            "current": round(current_price, 2),
            "past": round(past_price, 2),
            "change_pct": round(change_pct, 2),
        }

    return changes


def get_price_summary(ticker: str, is_commodity: bool = False) -> dict:

    df = get_stock_data(ticker, period_days=100)

    if df.empty:
        return {"error": "No data available"}

    info = get_stock_info(ticker)

    usd_inr = None

    # Commodity USD -> INR Conversion
    if is_commodity:
    
        usd_inr = get_usd_inr_rate()
    
        try:
    
            for col in ["Open", "High", "Low", "Close"]:
    
                if col in df.columns:
                    df[col] = df[col] * usd_inr
    
            # Convert 52W High & Low to INR
            for key in ["52w_high", "52w_low"]:
    
                value = info.get(key)
    
                if isinstance(value, (int, float)):
                    info[key] = round(value * usd_inr, 2)
    
            # Force current price from converted dataframe
            if not df.empty:
    
                info["current_price"] = round(
                    float(df["Close"].dropna().iloc[-1]),
                    2
                )
    
        except Exception as e:
    
            print(f"Commodity Conversion Error: {e}")

    price_changes = calculate_price_changes(df)

    # Stock fallback current price
    try:

        if (
            info.get("current_price") in [None, "N/A"]
            and not df.empty
        ):

            info["current_price"] = round(
                float(df["Close"].dropna().iloc[-1]),
                2
            )

    except Exception:
        pass

    return {
        "info": info,
        "price_changes": price_changes,
        "dataframe": df,
        "usd_inr_rate": usd_inr,
    }
