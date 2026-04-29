import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os
import time

# 強制指定 .env 的路徑
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")
# print("API_KEY loaded:", API_KEY[:8] + "..." if API_KEY else "❌ 空的")
BASE_URL = "https://www.alphavantage.co/query"


def get_stock_info(symbol: str) -> dict:
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    res = requests.get(BASE_URL, params=params)
    data = res.json()

    print("API 回傳：", data.get("Symbol"), data.get("Name"))

    if not data or "Symbol" not in data:
        return {
            "股票代號": symbol,
            "公司名稱": "N/A",
            "目前股價": "N/A",
            "52週最高": "N/A",
            "52週最低": "N/A",
            "市值": "N/A",
            "本益比": "N/A",
        }

    # 用 200日移動平均當作近似股價（OVERVIEW 沒有即時股價）
    price = float(data.get("200DayMovingAverage", 0))

    return {
        "股票代號": symbol,
        "公司名稱": data.get("Name", "N/A"),
        "目前股價": price,
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
    
    time.sleep(12)  # ← 加這行，等 12 秒再打第二個請求
    
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
