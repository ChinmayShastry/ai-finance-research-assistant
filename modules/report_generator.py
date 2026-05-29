from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def generate_long_term_report(
    asset_name: str,
    price_changes: dict,
    articles: list[dict],
    stock_info: dict,
) -> str:
    """Generate a long-term analysis report for the asset."""
    price_context = _format_price_changes(price_changes)
    news_context = _format_articles_brief(articles[:20])
    info_context = _format_stock_info(stock_info)

    prompt = f"""You are a senior financial research analyst for Indian markets.

Generate a LONG-TERM ANALYSIS REPORT for "{asset_name}".

Stock/Commodity Info:
{info_context}

Price Performance:
{price_context}

Recent News & Developments:
{news_context}

Write a concise report (200-300 words) covering:
1. Key price changes and trends over recent months
2. Probable reasons for these changes (macro, sector-specific, company-specific)
3. How the asset has performed relative to its sector

Keep it factual and data-driven. Use INR for all prices. No speculation beyond what the data supports."""

    return _call_openai(prompt)


def generate_upcoming_factors_report(
    asset_name: str,
    articles: list[dict],
    stock_info: dict,
) -> str:
    """Generate a report on upcoming factors that could affect the asset."""
    news_context = _format_articles_brief(articles[:15])
    info_context = _format_stock_info(stock_info)

    prompt = f"""You are a forward-looking financial analyst for Indian markets.

Based on recent news and developments about "{asset_name}", identify UPCOMING FACTORS that could affect its stock/commodity price.

Asset Info:
{info_context}

Recent News & Developments:
{news_context}

Write a concise report (150-250 words) covering:
1. Upcoming events (earnings, policy changes, regulatory decisions)
2. Macro factors (RBI policy, global trends, sector headwinds/tailwinds)
3. Company-specific catalysts (product launches, expansions, management changes)
4. Risks to watch out for

Be specific and actionable. Only mention factors with reasonable evidence from the news. If no clear upcoming factors are visible, say so honestly."""

    return _call_openai(prompt)


def _format_price_changes(price_changes: dict) -> str:
    """Format price changes into readable text."""
    if not price_changes:
        return "No price data available."

    lines = []
    for period, data in price_changes.items():
        direction = "up" if data["change_pct"] > 0 else "down"
        lines.append(
            f"- {period}: INR {data['current']} ({direction} {abs(data['change_pct'])}% from INR {data['past']})"
        )
    return "\n".join(lines)


def _format_articles_brief(articles: list[dict]) -> str:
    """Format articles briefly for context."""
    if not articles:
        return "No recent news available."

    lines = []
    for article in articles:
        title = article.get("title", "")
        date = article.get("published_at", "")[:10]
        if title:
            lines.append(f"- [{date}] {title}")

    return "\n".join(lines)


def _format_stock_info(info: dict) -> str:
    """Format stock info into readable text."""
    if not info:
        return "No additional info available."

    lines = []
    if info.get("name"):
        lines.append(f"Name: {info['name']}")
    if info.get("sector"):
        lines.append(f"Sector: {info['sector']}")
    if info.get("industry"):
        lines.append(f"Industry: {info['industry']}")
    if info.get("market_cap"):
        mc = info["market_cap"]
        if mc > 1e12:
            lines.append(f"Market Cap: INR {mc/1e12:.2f} Lakh Cr")
        elif mc > 1e9:
            lines.append(f"Market Cap: INR {mc/1e9:.2f} Thousand Cr")
    if info.get("pe_ratio") and info["pe_ratio"] != "N/A":
        lines.append(f"P/E Ratio: {info['pe_ratio']:.2f}")
    if info.get("52w_high") and info["52w_high"] != "N/A":
        lines.append(f"52W High: INR {info['52w_high']}")
    if info.get("52w_low") and info["52w_low"] != "N/A":
        lines.append(f"52W Low: INR {info['52w_low']}")

    return "\n".join(lines) if lines else "No additional info available."


def _call_openai(prompt: str) -> str:
    """Make a call to OpenAI API."""
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert financial research analyst specializing in Indian equity and commodity markets. Provide data-driven, concise analysis in INR context."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=800,
            timeout=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating report: {str(e)}"
