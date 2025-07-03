# 📈 Stocks News Sentiment Analyser with Its Impact on Stocks

A web-based application that fetches recent stock-related news, analyzes sentiment using an AI model (FinBERT), and visualizes its impact on stock price fluctuations.

---

## 🔍 Overview

This project enables users to:
- Search for any listed stock (e.g., Adani, Reliance).
- Fetch the latest news articles related to that company.
- Analyze sentiment (Positive / Neutral / Negative) using a transformer-based model (FinBERT).
- Visualize percentage changes in stock prices in response to each news headline.
- Maintain a user dashboard with saved stocks and news.

---

## 🧠 Features

- ✅ **AI Sentiment Analysis** via `ProsusAI/finbert`
- 📊 **Price Impact Chart** using Chart.js
- 🔒 **User Login/Register System** (JSON-based user tracking)
- ⭐ **Personal Dashboard** to save and monitor favorite stocks
- 📰 **News Fetching** using [NewsAPI.org](https://newsapi.org/)
- 💹 **Stock Price Tracking** using [yFinance](https://pypi.org/project/yfinance/)

---

## 🛠️ Tech Stack

| Layer        | Tools & Libraries                      |
|--------------|----------------------------------------|
| Backend      | Python, Flask                          |
| Frontend     | HTML, CSS, JavaScript, Chart.js        |
| AI/ML Model  | `transformers`, FinBERT by ProsusAI     |
| APIs         | NewsAPI, yFinance                      |
| Auth & Data  | JSON File-based user data storage      |

---

## 🧪 How It Works

1. User selects a company via search bar or dropdown.
2. App fetches the last 20 news articles using NewsAPI.
3. Each article is analyzed for sentiment using FinBERT.
4. Corresponding stock price changes are calculated via yFinance.
5. All results are shown on the page with a graph and sentiment label.
6. Logged-in users can save stocks to their dashboard.

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/stocks-sentiment-analyzer.git
cd stocks-sentiment-analyzer

 - NEWS_API_KEY = "your_actual_api_key_here"
 - python3 app.py


