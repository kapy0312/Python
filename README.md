# 🐍 Python 學習作品集

從零開始學 Python 的全端開發作品集，包含兩個完整部署的專案。

---

## 📁 專案總覽

| 專案 | 技術棧 | 線上 Demo |
|---|---|---|
| 📈 股票 AI 分析系統 | FastAPI + React + Groq AI | [前端](https://stock-frontend-1hc8.onrender.com) / [API](https://stock-backend-1a9y.onrender.com) |
| 💼 個人記帳系統 | Django + React TypeScript | [前端](https://budget-frontend-xxxx.onrender.com) / [API](https://budget-backend-gn7i.onrender.com) |

---

## 📈 專案一：股票 AI 分析系統

一個結合股票資料查詢與 AI 分析的全端專案，支援台股與美股查詢，提供歷史走勢圖表與 AI 分析報告。

🔗 **線上 Demo：** [https://stock-frontend-1hc8.onrender.com](https://stock-frontend-1hc8.onrender.com)  
🔗 **後端 API：** [https://stock-backend-1a9y.onrender.com](https://stock-backend-1a9y.onrender.com)

### 🖥️ 功能介紹

- 🔍 **股票查詢**：輸入股票代號（如 `AAPL`、`2330.TW`）查詢基本資訊
- 📊 **K 線走勢圖**：顯示近期收盤價與 MA5、MA20 移動平均線
- 🤖 **AI 分析報告**：呼叫 Groq AI 針對股票近期走勢給出分析
- 📅 **彈性期間**：支援 1 個月 / 3 個月 / 1 年資料查詢
- 🕐 **查詢紀錄**：自動記錄查詢歷史，點擊可快速再次查詢

### 🛠️ 技術棧

| 技術 | 用途 |
|---|---|
| Python + FastAPI | API 伺服器 |
| yfinance | 歷史 K 線資料 |
| Alpha Vantage API | 公司基本資訊 |
| Groq API (LLaMA 3.3) | AI 股票分析 |
| pandas | 資料處理與移動平均計算 |
| PostgreSQL + psycopg2 | 查詢紀錄資料庫 |
| React + Vite | 前端框架 |
| Recharts | 股價走勢圖表 |
| Docker / Docker Compose | 容器化 |
| Render | 雲端部署 |

### 📡 API 端點

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/stock/{symbol}` | 基本資訊 + 統計摘要 + K線資料 |
| GET | `/stock/{symbol}/ai` | AI 分析報告 |
| GET | `/history` | 最近查詢紀錄 |
| GET | `/debug` | 確認環境變數是否設定 |

### 🚀 本地執行

```bash
# 複製專案
git clone https://github.com/kapy0312/Python.git
cd Python

# 啟動資料庫
docker run --name stock-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=stockdb -p 5433:5432 -d postgres:17

# 後端
cd stock-crawler
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload

# 前端（另開終端機）
cd stock-frontend
npm install
npm run dev
```

### 🔑 環境變數

```
ALPHA_VANTAGE_KEY=你的_key
GROQ_API_KEY=你的_key
DB_HOST=localhost
DB_PORT=5433
DB_NAME=stockdb
DB_USER=postgres
DB_PASSWORD=password
```

---

## 💼 專案二：個人記帳系統

一個支援收支管理、投資損益追蹤的個人財務系統，支援台股、美股、加密貨幣即時報價，並自動換算台幣匯率。

🔗 **線上 Demo：** [https://budget-frontend-xxxx.onrender.com](https://budget-frontend-xxxx.onrender.com)  
🔗 **後端 API：** [https://budget-backend-gn7i.onrender.com](https://budget-backend-gn7i.onrender.com)

### 🖥️ 功能介紹

- 💰 **收支記錄**：新增、刪除收支，支援分類管理
- 📊 **月收支統計**：近 6 個月收支長條圖
- 📈 **投資持倉**：台股、美股、加密貨幣損益計算
- 💱 **即時匯率**：美股自動換算台幣市值
- 🥧 **資產分配**：圓餅圖顯示各持倉比例
- 🏦 **總資產總覽**：淨資產、年度收支、投資損益

### 🛠️ 技術棧

| 技術 | 用途 |
|---|---|
| Python + Django 6 | 後端框架 |
| Django REST Framework | REST API |
| yfinance | 即時股價 |
| CoinGecko API | 加密貨幣報價 |
| PostgreSQL + psycopg2 | 資料庫 |
| React + Vite + TypeScript | 前端框架 |
| Recharts | 圖表視覺化 |
| Render | 雲端部署 |

### 📡 API 端點

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/api/categories/` | 分類列表 |
| GET/POST | `/api/transactions/` | 收支記錄 |
| GET | `/api/transactions/summary/` | 月收支統計 |
| GET/POST | `/api/investments/` | 投資持倉 |
| GET | `/api/investments/portfolio/` | 即時損益（含匯率） |
| GET | `/api/investments/overview/` | 資產總覽 |

### 🚀 本地執行

```bash
# 啟動資料庫
docker run --name budget-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=budgetdb -p 5434:5432 -d postgres:17

# 後端
cd budget-tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# 前端（另開終端機）
cd budget-frontend
npm install
npm run dev
```

### 🔑 環境變數

```
DB_HOST=localhost
DB_PORT=5434
DB_NAME=budgetdb
DB_USER=postgres
DB_PASSWORD=password
```

---

## 🔄 CI/CD

兩個專案都整合 GitHub Actions，每次 push 自動執行：

```
push 到 main
    ↓
GitHub Actions 跑四個測試 job：
  ✅ 股票後端模組測試
  ✅ 股票前端 Build 測試
  ✅ 記帳後端 Django 檢查
  ✅ 記帳前端 Build 測試
    ↓
全部通過 → Render 自動部署
```

---

## 📝 學習歷程

這是我從零開始學 Python 的作品集，主要學習：

- **後端**：FastAPI、Django、Django REST Framework
- **資料庫**：PostgreSQL、psycopg2、Django ORM、SQL 語法
- **AI**：Groq API、Prompt Engineering、LLaMA 3.3
- **前端**：React、Vite、TypeScript、Recharts
- **容器化**：Docker、Docker Compose
- **部署**：Render（Web Service + Static Site + PostgreSQL）
- **CI/CD**：GitHub Actions、GitHub Secrets
- **工具**：DBeaver、Repomix、yfinance、Alpha Vantage API