# 📈 股票 AI 分析系統

一個結合股票資料查詢與 AI 分析的全端專案，支援台股與美股查詢，提供歷史走勢圖表與 AI 分析報告。

🔗 **線上 Demo：** [https://stock-frontend-1hc8.onrender.com](https://stock-frontend-1hc8.onrender.com)  
🔗 **後端 API：** [https://stock-backend-1a9y.onrender.com](https://stock-backend-1a9y.onrender.com)

---

## 🖥️ 功能介紹

- 🔍 **股票查詢**：輸入股票代號（如 `AAPL`、`2330.TW`）查詢基本資訊
- 📊 **K 線走勢圖**：顯示近期收盤價與 MA5、MA20 移動平均線
- 🤖 **AI 分析報告**：呼叫 Groq AI 針對股票近期走勢給出分析
- 📅 **彈性期間**：支援 1 個月 / 3 個月 / 1 年資料查詢
- 🕐 **查詢紀錄**：自動記錄查詢歷史，點擊可快速再次查詢

---

## 🛠️ 技術棧

### 後端
| 技術 | 用途 |
|---|---|
| Python + FastAPI | API 伺服器 |
| yfinance | 歷史 K 線資料 |
| Alpha Vantage API | 公司基本資訊 |
| Groq API (LLaMA 3.3) | AI 股票分析 |
| pandas | 資料處理與移動平均計算 |
| PostgreSQL + psycopg2 | 查詢紀錄資料庫 |

### 前端
| 技術 | 用途 |
|---|---|
| React + Vite | 前端框架 |
| Recharts | 股價走勢圖表 |

### 部署
| 技術 | 用途 |
|---|---|
| Docker / Docker Compose | 容器化 |
| Render Web Service | 後端部署 |
| Render Static Site | 前端部署 |
| Render PostgreSQL | 雲端資料庫 |

---

## 📁 專案結構

```
Python/
├── stock-crawler/          # FastAPI 後端
│   ├── api.py              # 路由定義
│   ├── crawler.py          # 股票資料爬蟲
│   ├── analyzer.py         # 移動平均計算
│   ├── ai_analyzer.py      # Groq AI 分析
│   ├── database.py         # PostgreSQL 資料庫連線
│   ├── main.py             # 命令列工具
│   ├── Dockerfile
│   └── requirements.txt
│
├── stock-frontend/         # React 前端
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── StockCard.jsx
│   │   │   └── StockChart.jsx
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## 🚀 本地執行

### 方法一：Docker Compose（推薦）

```bash
# 複製專案
git clone https://github.com/kapy0312/Python.git
cd Python

# 建立環境變數檔案
cp stock-crawler/.env.example stock-crawler/.env
# 填入你的 API Key

# 啟動前端 + 後端
docker-compose up

# 另開終端機，啟動本地資料庫
docker run --name stock-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=stockdb -p 5433:5432 -d postgres:17
```

前端：http://localhost:5173  
後端：http://localhost:8000

---

### 方法二：手動執行

**後端**
```bash
cd stock-crawler
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
uvicorn api:app --reload
```

**前端**
```bash
cd stock-frontend
npm install
npm run dev
```

---

## 🔑 環境變數

在 `stock-crawler/.env` 建立以下設定：

```
ALPHA_VANTAGE_KEY=你的_key
GROQ_API_KEY=你的_key

# 資料庫（本地 Docker）
DB_HOST=localhost
DB_PORT=5433
DB_NAME=stockdb
DB_USER=postgres
DB_PASSWORD=password
```

| 變數 | 取得方式 |
|---|---|
| `ALPHA_VANTAGE_KEY` | [alphavantage.co](https://www.alphavantage.co/support/#api-key) 免費申請 |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) 免費申請 |

---

## 📡 API 端點

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/stock/{symbol}` | 基本資訊 + 統計摘要 + K線資料 |
| GET | `/stock/{symbol}/ai` | AI 分析報告 |
| GET | `/history` | 最近查詢紀錄 |
| GET | `/debug` | 確認環境變數是否設定 |

**範例**
```
GET /stock/AAPL?period=3mo
GET /stock/2330.TW?period=1y
GET /stock/AAPL/ai
GET /history?limit=10
```

---

## 🗄️ 資料庫

| 環境 | 資料庫 |
|---|---|
| 本地開發 | Docker 跑 PostgreSQL 17（port 5433） |
| 雲端部署 | Render PostgreSQL 託管服務 |

啟動 API 時自動建立資料表（`init_db()`），不需要手動建立。

---

## 📝 學習歷程

這是我從零開始學 Python 的第五個專案，主要學習：

- FastAPI 後端 API 設計
- yfinance 股票資料爬蟲
- Groq API Prompt Engineering
- React 前後端串接
- Docker / Docker Compose 容器化部署
- Render 雲端部署（Web Service + Static Site + PostgreSQL）
- PostgreSQL 資料庫串接（psycopg2）
- 本地與雲端環境變數分離管理