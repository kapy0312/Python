# api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crawler import get_stock_info, get_stock_history
from analyzer import calculate_moving_average, get_summary
from ai_analyzer import analyze_stock
from database import save_search_history, get_search_history, init_db

app = FastAPI(title="股票資料 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()   # ← 啟動時自動建表

# ── 首頁 ──────────────────────────────────────
@app.get("/")
def root():
    return {"message": "股票 API 運作中 🚀"}


# ── 主要端點：基本資訊 + 統計 + K線 ──────────
@app.get("/stock/{symbol}")
def get_stock(symbol: str, period: str = "3mo"):
    try:
        info = get_stock_info(symbol)
        df = get_stock_history(symbol, period)

        if df.empty:
            raise HTTPException(status_code=404, detail=f"找不到股票：{symbol}")

        df = calculate_moving_average(df)
        summary = get_summary(df)

        # Alpha Vantage 額度用完時，用 yfinance 資料補股價
        if info["目前股價"] == "N/A" or info["目前股價"] == 0:
            info["目前股價"] = float(df["Close"].iloc[-1])
            info["52週最高"] = float(df["High"].max())
            info["52週最低"] = float(df["Low"].min())

        # 整理近 60 筆 K 線
        history = []
        for date, row in df[["Open", "High", "Low", "Close", "Volume", "MA5", "MA20"]].tail(60).iterrows():
            history.append({
                "日期": str(date.date()),
                "開盤": row["Open"],
                "最高": row["High"],
                "最低": row["Low"],
                "收盤": row["Close"],
                "成交量": int(row["Volume"]),
                "MA5": None if str(row["MA5"]) == "nan" else row["MA5"],
                "MA20": None if str(row["MA20"]) == "nan" else row["MA20"],
            })

        # ← 加這行，查詢完自動存紀錄
        save_search_history(
            symbol=symbol,
            company=info.get("公司名稱", "N/A"),
            price=float(df["Close"].iloc[-1]),
            period=period
        )

        return {
            "基本資訊": info,
            "統計摘要": summary,
            "歷史資料": history,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── AI 分析 ───────────────────────────────────
@app.get("/stock/{symbol}/ai")
def get_ai_analysis(symbol: str, period: str = "3mo"):
    try:
        info = get_stock_info(symbol)
        df = get_stock_history(symbol, period)

        if df.empty:
            raise HTTPException(status_code=404, detail=f"找不到股票：{symbol}")

        df = calculate_moving_average(df)
        summary = get_summary(df)
        analysis = analyze_stock(info, summary)

        return {"股票代號": symbol, "AI分析": analysis}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── 環境變數確認 ──────────────────────────────
@app.get("/debug")
def debug():
    import os

    def mask(key):
        val = os.environ.get(key, "❌ 空的")
        return val[:8] + "..." if val != "❌ 空的" else val

    return {
        "ALPHA_VANTAGE_KEY": mask("ALPHA_VANTAGE_KEY"),
        "GROQ_API_KEY": mask("GROQ_API_KEY"),
    }

# ── 查詢歷史紀錄 ──────────────────────────────


@app.get("/history")
def get_history(limit: int = 10):
    """查詢最近搜尋過的股票"""
    records = get_search_history(limit)
    return {"查詢紀錄": records}
