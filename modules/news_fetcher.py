import requests
import feedparser
from datetime import datetime, timedelta
from config import NEWS_API_KEY


def fetch_newsapi(query: str, days: int = 30) -> list[dict]:
    """Fetch news articles from NewsAPI."""
    if not NEWS_API_KEY:
        return []

    from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "published_at": article.get("publishedAt", ""),
                    "url": article.get("url", ""),
                })
            return articles
    except Exception:
        pass

    return []


def fetch_google_news_rss(query: str) -> list[dict]:
    """Fetch news from Google News RSS feed."""
    encoded_query = requests.utils.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}+India+stock+market&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:20]:
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")

            articles.append({
                "title": entry.get("title", ""),
                "description": entry.get("summary", ""),
                "source": entry.get("source", {}).get("title", "Google News"),
                "published_at": published,
                "url": entry.get("link", ""),
            })
        return articles
    except Exception:
        pass

    return []


def get_news_for_asset(asset_name: str, days: int = 30) -> list[dict]:
    """Fetch news from all sources for a given asset."""
    all_articles = []

    newsapi_articles = fetch_newsapi(f"{asset_name} India stock market", days=days)
    all_articles.extend(newsapi_articles)

    google_articles = fetch_google_news_rss(asset_name)
    all_articles.extend(google_articles)

    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title_lower = article["title"].lower().strip()
        if title_lower not in seen_titles and article["title"]:
            seen_titles.add(title_lower)
            unique_articles.append(article)

    unique_articles.sort(
        key=lambda x: x.get("published_at", ""),
        reverse=True,
    )

    return unique_articles


def filter_news_by_period(articles: list[dict], days: int) -> list[dict]:
    """Filter articles to only include those within the specified period."""
    cutoff_date = datetime.now() - timedelta(days=days)

    filtered = []
    for article in articles:
        pub_date_str = article.get("published_at", "")
        if not pub_date_str:
            continue
        try:
            pub_date = datetime.strptime(pub_date_str[:10], "%Y-%m-%d")
            if pub_date >= cutoff_date:
                filtered.append(article)
        except ValueError:
            continue

    return filtered
