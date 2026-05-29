# 📊 AI Financial Research Assistant

An AI-powered financial research platform that combines market data, financial news, and Large Language Models (LLMs) to generate actionable investment insights for Indian stocks and commodities.

🚀 **Live Demo:** https://ai-finance-research-assistant.streamlit.app/

---

## 🌟 Overview

The AI Financial Research Assistant helps investors, traders, analysts, and finance enthusiasts quickly understand market movements by transforming raw financial data and news into structured AI-generated research reports.

Instead of manually analyzing dozens of news articles, market updates, and company developments, users can generate comprehensive financial insights within seconds.

The platform combines:

- 📈 Market Data Analysis
- 📰 News Intelligence
- 🧠 AI Sentiment Analysis
- 📋 Long-Term Research Reports
- 🔮 Future Catalyst & Risk Identification

to provide a consolidated research experience.

---

## 🎯 Problem Statement

Investment research often requires analyzing information from multiple sources:

- Historical price performance
- Market sentiment
- Company developments
- Sector trends
- Economic events
- News articles

Manually gathering and interpreting this information is time-consuming and can lead to information overload.

This project leverages Artificial Intelligence to automate the research process and generate concise, human-readable financial insights.

---

## 💡 How This AI Assistant Helps

The AI Financial Research Assistant is **not a stock recommendation engine**.

Instead, it acts as an AI-powered research companion that helps users:

✅ Save research time

✅ Understand market sentiment

✅ Identify key news impacting an asset

✅ Discover potential future catalysts

✅ Monitor investment risks

✅ Make more informed investment decisions

The final investment decision always remains with the investor.

---

## 🚀 Features

### 📈 Market Data Analysis

- Historical stock and commodity price tracking
- Price performance across multiple time horizons
- Interactive price charts
- Volume analysis and visualization

---

### 📰 News Intelligence Engine

Aggregates financial news from:

- NewsAPI
- Google News RSS

The platform automatically collects and processes relevant news articles related to the selected asset.

---

### 🧠 AI Sentiment Analysis

Using OpenAI GPT models, the assistant analyzes financial news and generates sentiment summaries across:

- 7 Days
- 30 Days
- 90 Days

The analysis highlights:

- Bullish sentiment
- Bearish sentiment
- Neutral sentiment
- Key drivers influencing investor behavior

---

### 📋 Long-Term Research Report

The AI generates a comprehensive research report covering:

- Recent price trends
- Company developments
- Sector performance
- Macro-economic influences
- Probable reasons behind price movements

---

### 🔮 Upcoming Factors & Risk Analysis

The assistant identifies future events and catalysts that may impact the selected asset.

Examples include:

- Earnings announcements
- Regulatory changes
- RBI policy decisions
- Industry developments
- Product launches
- Expansion plans
- Global economic trends

This helps users understand potential opportunities and risks before making investment decisions.

---

## 📊 Supported Assets

### Stocks

- Nifty 250 Companies
- Major Indian Listed Companies

### Commodities

- Gold
- Silver
- Crude Oil
- Natural Gas
- Copper
- Zinc
- Aluminium
- Nickel
- Cotton
- Mentha Oil

---

## 🏗️ System Architecture

```text
User
  │
  ▼
Streamlit Interface
  │
  ├── Yahoo Finance
  │       │
  │       ▼
  │   Market Data
  │
  ├── NewsAPI
  │
  ├── Google News RSS
  │       │
  │       ▼
  │   News Aggregation
  │
  ▼
OpenAI GPT-4o-mini
  │
  ├── Sentiment Analysis
  ├── Long-Term Research Report
  └── Upcoming Factors Analysis
  │
  ▼
Research Dashboard
```

---

## 🛠️ Technology Stack

### Frontend

- Streamlit

### Data Sources

- Yahoo Finance
- NewsAPI
- Google News RSS

### AI & LLM

- OpenAI GPT-4o-mini

### Data Processing

- Pandas

### Visualization

- Plotly

---

## 📸 Screenshots

### Dashboard Overview

![Dashboard](screenshots/dashboard.png)

---

### AI Sentiment Analysis

![Sentiment Analysis](screenshots/sentiment_analysis.png)

---

### Long-Term Research Report

![Long Term Report](screenshots/long_term_report.png)

---

### Upcoming Factors & Risk Analysis

![Upcoming Factors](screenshots/upcoming_factors.png)

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/ChinmayShastry/ai-finance-research-assistant.git

cd ai-finance-research-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_newsapi_key
```

### Run the Application

```bash
streamlit run app.py
```

---

## 🎯 Future Enhancements

- Portfolio Tracking
- Watchlists
- Technical Indicator Analysis
- RAG-Powered Financial Knowledge Base
- Earnings Transcript Analysis
- Multi-Agent Financial Research Workflows
- Real-Time Market Monitoring
- Institutional Grade Report Generation

---

## ⚠️ Disclaimer

This project is intended for educational and research purposes only.

The information generated by this application should not be considered financial, investment, or trading advice.

Always conduct your own research and consult qualified financial professionals before making investment decisions.

---

## 👨‍💻 Author

**Chinmay Shastry**

AI/ML Engineer | Generative AI | RAG Systems | Financial AI Applications

GitHub: https://github.com/ChinmayShastry

---

⭐ If you found this project useful, consider starring the repository.
