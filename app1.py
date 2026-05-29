import streamlit as st

st.write("START")

from config import *

st.write("CONFIG OK")

from modules.market_data import *

st.write("MARKET OK")

from modules.news_fetcher import *

st.write("NEWS OK")

from modules.sentiment_analyzer import *

st.write("SENTIMENT OK")

from modules.report_generator import *

st.write("REPORT OK")
