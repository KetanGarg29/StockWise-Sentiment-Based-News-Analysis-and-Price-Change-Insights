from flask import Flask, request, render_template, redirect, url_for, session
import requests
from datetime import datetime, timedelta
import yfinance as yf
import json
import os
from transformers import pipeline

# Setup
app = Flask(__name__)
app.secret_key = 'very-secret-key'  # Required for session management

NEWS_API_KEY = "Your Api Key"
sentiment_pipe = pipeline("text-classification", model="ProsusAI/finbert")


# ──────────────────────────────────────────────────────────────
# Helpers

def load_db():
    if not os.path.exists("db.json"):
        with open("db.json", "w") as f:
            json.dump({"users": {}}, f)
    with open("db.json", "r") as f:
        return json.load(f)


def save_db(db):
    with open("db.json", "w") as f:
        json.dump(db, f, indent=2)


def get_symbol_from_name(company_name):
    try:
        with open(os.path.join('static', 'stocks.json'), 'r') as f:
            stocks = json.load(f)

        company_name_lower = company_name.lower()

        for stock in stocks:
            if company_name_lower in stock['name'].lower():
                return stock['symbol']

        return None
    except Exception as e:
        print(f"[ERROR loading stock symbol]: {e}")
        return None


def get_stock_change_on_date(symbol, date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        next_day = date + timedelta(days=1)
        stock = yf.Ticker(symbol)

        hist = stock.history(start=date_str, end=next_day.strftime('%Y-%m-%d'))
        if hist.empty:
            return None

        open_price = hist.iloc[0]['Open']
        close_price = hist.iloc[0]['Close']
        percent_change = ((close_price - open_price) / open_price) * 100
        return round(percent_change, 2)
    except Exception as e:
        print(f"[ERROR in stock change]: {e}")
        return None


def fetch_recent_news(company_name):
    today = datetime.utcnow()
    from_date = today - timedelta(days=14)

    query = f"{company_name}"

    url = (
        f"https://newsapi.org/v2/everything?qInTitle={query}"
        f"&from={from_date.date()}&to={today.date()}"
        f"&sortBy=publishedAt&language=en&pageSize=20&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()
    print(f"[DEBUG] NewsAPI status: {response.status_code}")
    print(f"[DEBUG] NewsAPI response: {data}")

    if response.status_code != 200 or "articles" not in data:
        return []

    symbol = get_symbol_from_name(company_name)

    news = []
    for article in data["articles"]:
        pub_date = article["publishedAt"][:10]
        change = get_stock_change_on_date(symbol, pub_date)
        change_str = f"{change:+.2f}%" if change is not None else "N/A"

        text_to_analyze = article["title"] + " " + article.get("description", "")
        try:
            sentiment_result = sentiment_pipe(text_to_analyze, truncation=True)[0]
            sentiment_label = sentiment_result["label"].capitalize()
        except Exception as e:
            print(f"[ERROR in sentiment analysis]: {e}")
            sentiment_label = "Unknown"

        news.append({
            "title": article["title"],
            "description": article.get("description", ""),
            "url": article["url"],
            "publishedAt": pub_date,
            "source": article["source"]["name"],
            "stock_change": change_str,
            "sentiment": sentiment_label
        })

    return news


# ──────────────────────────────────────────────────────────────
# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    news_data = []
    company = ""

    if request.method == 'POST':
        company = request.form.get('company', '').strip()
        if company:
            session['last_company'] = company
            news_data = fetch_recent_news(company)

    return render_template('index.html', news=news_data, company=company)


@app.route('/add_to_dashboard', methods=['POST'])
def add_to_dashboard():
    company = session.get('last_company')
    username = session.get('username')

    if not company or not username:
        return redirect(url_for('index'))

    db = load_db()
    if username not in db["users"]:
        db["users"][username] = []

    if company not in db["users"][username]:
        db["users"][username].append(company)

    save_db(db)
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    db = load_db()
    user_stocks = db["users"].get(username, [])

    dashboard_data = []
    for stock in user_stocks:
        news = fetch_recent_news(stock)
        dashboard_data.append({"company": stock, "news": news})

    return render_template('dashboard.html', dashboard_data=dashboard_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
