# crawler.py

import requests
import yfinance as yf
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")
BASE_URL = "https://www.alphavantage.co/query"


def get_stock_info(symbol: str) -> dict:
    """基本資訊：優先 Alpha Vantage，額度用完自動改用 yfinance"""

    # ── 先試 Alpha Vantage ──────────────────────
    try:
        res = requests.get(BASE_URL, params={
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_KEY,
        }, timeout=10)
        data = res.json()

        if "Symbol" in data:
            return {
                "股票代號": symbol,
                "公司名稱": data.get("Name", "N/A"),
                "目前股價": float(data.get("200DayMovingAverage") or 0),
                "52週最高": float(data.get("52WeekHigh") or 0),
                "52週最低": float(data.get("52WeekLow") or 0),
                "市值": data.get("MarketCapitalization", "N/A"),
                "本益比": data.get("PERatio", "N/A"),
            }

        print(f"⚠️ Alpha Vantage 無資料，改用 yfinance 備援")

    except Exception as e:
        print(f"⚠️ Alpha Vantage 錯誤: {e}，改用 yfinance 備援")

    # ── Alpha Vantage 失敗 → yfinance 備援 ──────
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info  # yfinance 的基本資訊

        return {
            "股票代號": symbol,
            "公司名稱": info.get("longName") or info.get("shortName") or symbol,
            "目前股價": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
            "52週最高": info.get("fiftyTwoWeekHigh") or 0,
            "52週最低": info.get("fiftyTwoWeekLow") or 0,
            "市值": str(info.get("marketCap", "N/A")),
            "本益比": str(info.get("trailingPE", "N/A")),
        }

    except Exception as e:
        print(f"❌ yfinance 備援也失敗: {e}")
        return {
            "股票代號": symbol,
            "公司名稱": symbol,   # 最後保底：直接顯示代號
            "目前股價": 0,
            "52週最高": 0,
            "52週最低": 0,
            "市值": "N/A",
            "本益比": "N/A",
        }


def get_stock_history(symbol: str, period: str = "3mo") -> pd.DataFrame:
    try:
        # yf.download 比 Ticker.history 在雲端更穩定
        df = yf.download(
            symbol,
            period=period,
            progress=False,   # 關掉進度條
            auto_adjust=True  # 自動調整除權息
        )

        if df.empty:
            print(f"⚠️ yfinance 回傳空資料: {symbol}")
            return pd.DataFrame()

        # yf.download 回傳多層欄位，需要壓平
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df.round(2)

    except Exception as e:
        print(f"❌ get_stock_history 錯誤: {e}")
        return pd.DataFrame()


def save_to_csv(df: pd.DataFrame, symbol: str) -> str:
    """把歷史資料存成 CSV 檔案"""
    from datetime import datetime

    os.makedirs("data", exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/{symbol}_{today}.csv"
    df.to_csv(filename, encoding="utf-8-sig")
    print(f"✅ 已儲存：{filename}")
    return filename
