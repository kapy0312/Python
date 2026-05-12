# tracker/price_fetcher.py

import yfinance as yf
import requests


def get_stock_price(symbol: str) -> float:
    """
    抓取股票即時價格
    台股：2330.TW
    美股：AAPL
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        return float(price)
    except Exception as e:
        print(f"❌ 抓取股價失敗 {symbol}: {e}")
        return 0.0


def get_crypto_price(symbol: str) -> float:
    """
    抓取加密貨幣即時價格（CoinGecko API）
    symbol：bitcoin、ethereum、solana...
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": symbol.lower(),
            "vs_currencies": "usd"
        }
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        price = data.get(symbol.lower(), {}).get("usd", 0)
        return float(price)
    except Exception as e:
        print(f"❌ 抓取幣價失敗 {symbol}: {e}")
        return 0.0


def get_price(investment_type: str, symbol: str) -> float:
    """
    統一入口，依照投資類型選擇 API
    """
    if investment_type == "crypto":
        return get_crypto_price(symbol)
    else:
        return get_stock_price(symbol)   # 台股 + 美股都用 yfinance


def get_usd_to_twd() -> float:
    """抓取即時美元對台幣匯率"""
    try:
        ticker = yf.Ticker("USDTWD=X")
        info = ticker.info
        rate = info.get("regularMarketPrice") or info.get("bid") or 31.0
        return float(rate)
    except Exception as e:
        print(f"❌ 抓取匯率失敗: {e}")
        return 31.0  # 失敗時用預設值
