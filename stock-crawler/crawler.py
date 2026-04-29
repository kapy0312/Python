import yfinance as yf
import requests
import pandas as pd
from datetime import datetime
import os


def get_stock_info(symbol: str) -> dict:
    """
    抓取股票的基本資訊

    symbol: 股票代號
    - 台股要加 .TW，例如 台積電 = "2330.TW"
    - 美股直接輸入，例如 蘋果 = "AAPL"
    """

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    # 建立 yfinance 的股票物件
    stock = yf.Ticker(symbol)

    # .info 是一個字典，裡面有公司名稱、市值、本益比等資訊
    info = stock.info

    # 我們只取我們需要的欄位，避免資訊過多
    return {
        "股票代號": symbol,
        "公司名稱": info.get("longName", "N/A"),
        "目前股價": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
        "52週最高": info.get("fiftyTwoWeekHigh", "N/A"),
        "52週最低": info.get("fiftyTwoWeekLow", "N/A"),
        "市值": info.get("marketCap", "N/A"),
        "本益比": info.get("trailingPE", "N/A"),
    }


def get_stock_history(symbol: str, period: str = "3mo") -> pd.DataFrame:
    """
    抓取股票的歷史價格

    period 可以是：
    - "1mo"  = 最近一個月
    - "3mo"  = 最近三個月（預設）
    - "1y"   = 最近一年
    - "5y"   = 最近五年
    """

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    stock = yf.Ticker(symbol)

    # .history() 回傳一個 DataFrame（可以想像成 Excel 的工作表）
    # 欄位包含：Open（開盤）, High（最高）, Low（最低）, Close（收盤）, Volume（成交量）
    df = stock.history(period=period)

    # 把日期格式整理乾淨（去掉時區資訊，只保留日期）
    df.index = df.index.tz_localize(None)

    # 四捨五入到小數點後兩位，讓數字更好看
    df = df.round(2)

    return df


def save_to_csv(df: pd.DataFrame, symbol: str) -> str:
    """
    把 DataFrame 儲存成 CSV 檔案
    回傳儲存的檔案路徑
    """
    # 確保 data 資料夾存在，如果不存在就建立
    os.makedirs("data", exist_ok=True)

    # 用日期當檔名，避免每次執行都覆蓋同一個檔案
    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/{symbol}_{today}.csv"

    df.to_csv(filename, encoding="utf-8-sig")  # utf-8-sig 讓 Excel 能正確顯示中文

    return filename
