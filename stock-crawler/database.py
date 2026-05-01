# database.py

import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")


def get_connection():
    """建立資料庫連線"""
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5433"),
        database=os.environ.get("DB_NAME", "stockdb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "password"),
    )


def save_search_history(symbol: str, company: str, price: float, period: str):
    """把查詢紀錄寫進資料庫"""
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO search_history (symbol, company, price, period)
            VALUES (%s, %s, %s, %s)
        """, (symbol, company, price, period))

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ 已記錄查詢：{symbol}")

    except Exception as e:
        print(f"❌ 資料庫寫入失敗：{e}")


def get_search_history(limit: int = 10) -> list:
    """查詢最近的搜尋紀錄"""
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT symbol, company, price, period, searched_at
            FROM search_history
            ORDER BY searched_at DESC
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "股票代號": row[0],
                "公司名稱": row[1],
                "查詢價格": row[2],
                "查詢期間": row[3],
                "查詢時間": str(row[4]),
            }
            for row in rows
        ]

    except Exception as e:
        print(f"❌ 資料庫查詢失敗：{e}")
        return []


def init_db():
    """啟動時自動建立表格（如果不存在）"""
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id          SERIAL PRIMARY KEY,
                symbol      VARCHAR(20)  NOT NULL,
                company     VARCHAR(100),
                price       NUMERIC(10,2),
                period      VARCHAR(10),
                searched_at TIMESTAMP DEFAULT NOW()
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ 資料庫初始化完成")

    except Exception as e:
        print(f"❌ 資料庫初始化失敗：{e}")
