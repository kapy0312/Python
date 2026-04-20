from tabulate import tabulate
from crawler import get_stock_info, get_stock_history, save_to_csv
from analyzer import calculate_moving_average, get_summary

def main():
    print("=" * 50)
    print("      📈 股票資料分析工具")
    print("=" * 50)
    
    # 讓使用者輸入股票代號
    symbol = input("\n請輸入股票代號（台股加 .TW，例如 2330.TW）：").strip().upper()
    period = input("查詢期間（1mo / 3mo / 1y，直接按 Enter 預設 3mo）：").strip() or "3mo"
    
    print(f"\n⏳ 正在抓取 {symbol} 的資料...\n")

    # --- 抓基本資訊 ---
    try:
        info = get_stock_info(symbol)
        
        print("【基本資訊】")
        # 把字典轉成 [key, value] 的格式讓 tabulate 印出
        info_table = [[k, v] for k, v in info.items()]
        print(tabulate(info_table, tablefmt="rounded_outline"))
        
    except Exception as e:
        print(f"⚠️  抓取基本資訊失敗：{e}")

    # --- 抓歷史資料 ---
    try:
        df = get_stock_history(symbol, period)
        
        if df.empty:
            print("❌ 找不到股票資料，請確認代號是否正確")
            return
        
        # 計算移動平均線
        df = calculate_moving_average(df)
        
        # 顯示最新 5 筆資料
        print("\n【最近 5 天行情】")
        recent = df[["Open", "High", "Low", "Close", "Volume", "MA5", "MA20"]].tail(5)
        print(tabulate(recent, headers="keys", tablefmt="rounded_outline", floatfmt=".2f"))
        
        # 顯示統計摘要
        print("\n【統計摘要】")
        summary = get_summary(df)
        summary_table = [[k, v] for k, v in summary.items()]
        print(tabulate(summary_table, tablefmt="rounded_outline"))
        
        # 儲存完整資料
        filepath = save_to_csv(df, symbol)
        print(f"\n✅ 完整資料已儲存至：{filepath}")
        
    except Exception as e:
        print(f"⚠️  發生錯誤：{e}")

# 這個 if 判斷式是 Python 的慣例寫法
# 意思是：只有「直接執行這個檔案」時才跑 main()
# 如果這個檔案被其他程式 import，就不會自動執行
if __name__ == "__main__":
    main()