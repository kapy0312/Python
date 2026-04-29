from fastapi import FastAPI, HTTPException
from crawler import get_stock_info, get_stock_history
from analyzer import calculate_moving_average, get_summary
from ai_analyzer import analyze_stock   # ← 加在最上面的 import
from fastapi.middleware.cors import CORSMiddleware

# 建立 FastAPI 應用程式
app = FastAPI(title="股票資料 API", version="1.0.0")

# 加在 app 建立後面
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 之後換成你的 Render 前端網址
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """首頁，確認 API 有在運作"""
    return {"message": "股票 API 運作中 🚀"}


@app.get("/stock/{symbol}")
def get_stock(symbol: str, period: str = "3mo"):
    """
    查詢股票基本資訊 + 統計摘要

    - symbol: 股票代號，例如 2330.TW 或 AAPL
    - period: 查詢期間，預設 3mo（可傳 1mo / 3mo / 1y）
    """
    try:
        # 抓基本資訊
        info = get_stock_info(symbol)

        # 抓歷史資料並計算移動平均
        df = get_stock_history(symbol, period)

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"找不到股票：{symbol}"
            )

        df = calculate_moving_average(df)
        summary = get_summary(df)

        return {
            "基本資訊": info,
            "統計摘要": summary,
        }

    except HTTPException:
        raise  # 把 404 原封不動往上拋
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stock/{symbol}/history")
def get_history(symbol: str, period: str = "3mo"):
    """
    查詢股票歷史價格（最近 10 筆）
    """
    try:
        df = get_stock_history(symbol, period)

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"找不到股票：{symbol}"
            )

        df = calculate_moving_average(df)

        # 取最近 10 筆，轉成 dict 格式回傳
        recent = df[["Open", "High", "Low", "Close",
                     "Volume", "MA5", "MA20"]].tail(10)

        # 把 DataFrame 轉成 JSON 可以接受的格式
        result = []
        for date, row in recent.iterrows():
            result.append({
                "日期": str(date.date()),
                "開盤": row["Open"],
                "最高": row["High"],
                "最低": row["Low"],
                "收盤": row["Close"],
                "成交量": int(row["Volume"]),
                "MA5": row["MA5"] if not str(row["MA5"]) == "nan" else None,
                "MA20": row["MA20"] if not str(row["MA20"]) == "nan" else None,
            })

        return {"股票代號": symbol, "歷史資料": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stock/{symbol}/ai")
def get_ai_analysis(symbol: str, period: str = "3mo"):
    """
    用 AI 分析股票資料
    """
    try:
        info = get_stock_info(symbol)
        df = get_stock_history(symbol, period)

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"找不到股票：{symbol}"
            )

        df = calculate_moving_average(df)
        summary = get_summary(df)

        # 呼叫 AI 分析
        analysis = analyze_stock(info, summary)

        return {
            "股票代號": symbol,
            "AI分析": analysis
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/debug")
def debug():
    import os
    return {
        "ALPHA_VANTAGE_KEY": os.environ.get("ALPHA_VANTAGE_KEY", "❌ 空的")[:8] + "...",
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", "❌ 空的")[:8] + "...",
    }
