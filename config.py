import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

OPENAI_MODEL = "gpt-4o-mini"

SENTIMENT_PERIODS = {
    "7 Days": 7,
    "30 Days": 30,
    "90 Days": 90,
}
