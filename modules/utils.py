import pandas as pd
import plotly.graph_objects as go


def format_market_cap(value: float) -> str:
    """Format market cap in Indian number system."""
    if not value or value == 0:
        return "N/A"
    if value >= 1e12:
        return f"₹{value/1e12:.2f} Lakh Cr"
    elif value >= 1e9:
        return f"₹{value/1e7:.0f} Cr"
    elif value >= 1e7:
        return f"₹{value/1e7:.2f} Cr"
    else:
        return f"₹{value:,.0f}"


def create_price_chart(df: pd.DataFrame, title: str) -> go.Figure:
    """Create an interactive price chart using Plotly."""
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price",
    ))

    fig.update_layout(
        title=title,
        yaxis_title="Price (INR)",
        xaxis_title="Date",
        template="plotly_dark",
        height=400,
        xaxis_rangeslider_visible=False,
    )

    return fig


def create_volume_chart(df: pd.DataFrame, title: str) -> go.Figure:
    """Create a volume bar chart."""
    colors = ["green" if row["Close"] >= row["Open"] else "red" for _, row in df.iterrows()]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Date"],
        y=df["Volume"],
        marker_color=colors,
        name="Volume",
    ))

    fig.update_layout(
        title=title,
        yaxis_title="Volume",
        xaxis_title="Date",
        template="plotly_dark",
        height=250,
    )

    return fig


def color_change(value: float) -> str:
    """Return colored text for price change."""
    if value > 0:
        return f"🟢 +{value:.2f}%"
    elif value < 0:
        return f"🔴 {value:.2f}%"
    else:
        return f"⚪ {value:.2f}%"
