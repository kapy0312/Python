import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os

# 強制指定 .env 的路徑
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")
# print("API_KEY loaded:", API_KEY[:8] + "..." if API_KEY else "❌ 空的")
BASE_URL = "https://www.alphavantage.co/query"


def get_stock_info(symbol: str) -> dict:
    """
    抓取股票基本資訊
    Alpha Vantage 的股票代號格式：
    台股：2330.TW → 不支援，改用美股
    美股：AAPL、TSLA、NVDA
    """
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    res = requests.get(BASE_URL, params=params)
    data = res.json()

    print("API 回傳：", data)  # ← 加這行

    if not data or "Symbol" not in data:
        return {
            "股票代號": symbol,
            "公司名稱": "N/A",
            "目前股價": "N/A",
            "52週最高": data.get("52WeekHigh", "N/A"),
            "52週最低": data.get("52WeekLow", "N/A"),
            "市值": data.get("MarketCapitalization", "N/A"),
            "本益比": data.get("PERatio", "N/A"),
        }

    # 另外抓即時股價
    price_params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    price_res = requests.get(BASE_URL, params=price_params)
    price_data = price_res.json().get("Global Quote", {})

    return {
        "股票代號": symbol,
        "公司名稱": data.get("Name", "N/A"),
        "目前股價": float(price_data.get("05. price", 0)),
        "52週最高": float(data.get("52WeekHigh", 0)),
        "52週最低": float(data.get("52WeekLow", 0)),
        "市值": data.get("MarketCapitalization", "N/A"),
        "本益比": data.get("PERatio", "N/A"),
    }


def get_stock_history(symbol: str, period: str = "3mo") -> pd.DataFrame:
    """
    抓取股票歷史價格
    period: 1mo / 3mo / 1y
    """
    # 依照 period 決定抓多少資料
    if period == "1mo":
        av_function = "TIME_SERIES_DAILY"
        outputsize = "compact"   # 最近 100 筆
    elif period == "3mo":
        av_function = "TIME_SERIES_DAILY"
        outputsize = "compact"
    else:
        av_function = "TIME_SERIES_DAILY"
        outputsize = "full"      # 完整歷史

    params = {
        "function": av_function,
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": API_KEY,
    }

    res = requests.get(BASE_URL, params=params)
    data = res.json()

    print("歷史資料回傳 keys：", list(data.keys()))  # ← 加這行
    print("歷史資料內容前100字：", str(data)[:100])  # ← 加這行

    time_series = data.get("Time Series (Daily)", {})

    if not time_series:
        return pd.DataFrame()

    rows = []
    for date_str, values in time_series.items():
        rows.append({
            "Date": pd.to_datetime(date_str),
            "Open":   float(values["1. open"]),
            "High":   float(values["2. high"]),
            "Low":    float(values["3. low"]),
            "Close":  float(values["4. close"]),
            "Volume": int(values["5. volume"]),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("Date").set_index("Date")

    # 依照 period 篩選時間範圍
    now = pd.Timestamp.now()
    if period == "1mo":
        df = df[df.index >= now - pd.DateOffset(months=1)]
    elif period == "3mo":
        df = df[df.index >= now - pd.DateOffset(months=3)]

    return df.round(2)


def save_to_csv(df: pd.DataFrame, symbol: str) -> str:
    import os
    os.makedirs("data", exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/{symbol}_{today}.csv"
    df.to_csv(filename, encoding="utf-8-sig")
    return filename
