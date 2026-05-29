from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_sentiment_for_period(asset_name: str, articles: list[dict], period_label: str) -> str:
    """Generate a brief sentiment summary for a given period using OpenAI."""
    if not articles:
        return f"No news data available for {period_label}."

    news_text = _format_articles_for_prompt(articles[:15])

    prompt = f"""You are a financial sentiment analyst for Indian markets.
Analyze the following news articles about "{asset_name}" from the past {period_label}.

Give a BRIEF sentiment summary (3-5 sentences max) covering:
1. Overall market sentiment (Bullish/Bearish/Neutral)
2. Key factors driving the sentiment
3. What traders/investors are thinking

News Articles:
{news_text}

Respond concisely. No bullet points, no headers - just a flowing brief paragraph."""

    return _call_openai(prompt)


def generate_sentiment_report(asset_name: str, period_sentiments: dict) -> str:
    """Combine period sentiments into a structured report."""
    report_parts = []
    for period, sentiment in period_sentiments.items():
        report_parts.append(f"**{period}:**\n{sentiment}\n")

    return "\n".join(report_parts)


def _format_articles_for_prompt(articles: list[dict]) -> str:
    """Format articles into a readable string for the prompt."""
    lines = []
    for i, article in enumerate(articles, 1):
        title = article.get("title", "")
        desc = article.get("description", "")
        source = article.get("source", "")
        date = article.get("published_at", "")[:10]

        lines.append(f"{i}. [{date}] {title} ({source})")
        if desc:
            lines.append(f"   {desc[:200]}")

    return "\n".join(lines)


def _call_openai(prompt: str) -> str:
    """Make a call to OpenAI API."""
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a concise financial analyst specializing in Indian markets. Always respond in brief, actionable insights."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating analysis: {str(e)}"
