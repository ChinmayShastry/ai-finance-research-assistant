import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

OPENAI_MODEL = "gpt-4o-mini"

SENTIMENT_PERIODS = {
    "5 Days": 5,
    "15 Days": 15,
    "30 Days": 30,
    "3 Months": 90,
}
