import pandas as pd

def calculate_moving_average(df: pd.DataFrame) -> pd.DataFrame:
    """
    計算移動平均線（MA）
    
    移動平均是技術分析最基本的指標
    MA5  = 過去 5 天的平均收盤價（短期趨勢）
    MA20 = 過去 20 天的平均收盤價（中期趨勢）
    """
    df = df.copy()  # 複製一份，不修改原始資料（好習慣）
    
    # pandas 的 rolling(n).mean() 就是計算移動平均
    df["MA5"]  = df["Close"].rolling(window=5).mean().round(2)
    df["MA20"] = df["Close"].rolling(window=20).mean().round(2)
    
    return df


def get_summary(df: pd.DataFrame) -> dict:
    """
    產生一份簡單的統計摘要
    """
    latest = df.iloc[-1]   # iloc[-1] 取最後一列（最新的一天）
    oldest = df.iloc[0]    # iloc[0]  取第一列（最舊的一天）
    
    # 計算期間漲跌幅（百分比）
    price_change = ((latest["Close"] - oldest["Close"]) / oldest["Close"]) * 100
    
    return {
        "分析期間":   f"{df.index[0].date()} ~ {df.index[-1].date()}",
        "起始收盤價": oldest["Close"],
        "最新收盤價": latest["Close"],
        "期間漲跌幅": f"{price_change:+.2f}%",  # :+.2f 讓正數也顯示 + 號
        "期間最高價": df["High"].max(),
        "期間最低價": df["Low"].min(),
        "平均成交量": f"{df['Volume'].mean():,.0f}",  # :, 讓數字加入千位逗號
    }