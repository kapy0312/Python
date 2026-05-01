import { useState, useEffect } from "react"   // ← 補上 useEffect
import StockCard from "./components/StockCard"
import StockChart from "./components/StockChart"
import "./App.css"

const API_URL = import.meta.env.VITE_API_URL || ""

function App() {
  const [symbol, setSymbol] = useState("")
  const [period, setPeriod] = useState("3mo")
  const [stockData, setStockData] = useState(null)
  const [historyData, setHistoryData] = useState([])
  const [aiAnalysis, setAiAnalysis] = useState("")
  const [loading, setLoading] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [error, setError] = useState("")
  const [history, setHistory] = useState([])   // ← 新增

  // ── 拉取查詢紀錄 ─────────────────────────────  ← 新增
  async function fetchHistory() {
    try {
      const res = await fetch(`${API_URL}/history?limit=5`)
      const data = await res.json()
      setHistory(data.查詢紀錄 || [])
    } catch (err) {
      console.error("無法取得查詢紀錄")
    }
  }

  // ── 頁面載入時自動拉取紀錄 ───────────────────  ← 新增
  useEffect(() => {
    fetchHistory()
  }, [])

  // ── 查詢股票 ────────────────────────────────
  async function handleSearch() {
    const s = symbol.trim().toUpperCase()
    if (!s) return

    setLoading(true)
    setError("")
    setStockData(null)
    setHistoryData([])
    setAiAnalysis("")

    try {
      const res = await fetch(`${API_URL}/stock/${s}?period=${period}`)

      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail || "找不到股票，請確認代號是否正確")
      }

      const data = await res.json()
      setStockData(data)
      setHistoryData(data.歷史資料 || [])

    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
      fetchHistory()   // ← 這行沒加到
    }
  }

  // ── AI 分析 ──────────────────────────────────
  async function handleAiAnalysis() {
    const s = symbol.trim().toUpperCase()
    if (!s) return

    setAiLoading(true)
    setAiAnalysis("")

    try {
      const res = await fetch(`${API_URL}/stock/${s}/ai?period=${period}`)

      if (!res.ok) throw new Error("AI 分析請求失敗")

      const data = await res.json()
      setAiAnalysis(data.AI分析 || "AI 未回傳結果")

    } catch (err) {
      setAiAnalysis("❌ AI 分析失敗，請稍後再試")
    } finally {
      setAiLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") handleSearch()
  }

  // ── 畫面 ─────────────────────────────────────
  return (
    <div className="container">
      <h1>📈 股票查詢系統</h1>

      {/* 搜尋列 */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="輸入股票代號，例如 2330.TW 或 AAPL"
          value={symbol}
          onChange={e => setSymbol(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <select value={period} onChange={e => setPeriod(e.target.value)}>
          <option value="1mo">1 個月</option>
          <option value="3mo">3 個月</option>
          <option value="1y">1 年</option>
        </select>
        <button onClick={handleSearch} disabled={loading}>
          {loading ? "查詢中..." : "查詢"}
        </button>
      </div>

      {/* 錯誤訊息 */}
      {error && <div className="error">⚠️ {error}</div>}

      {/* 查詢紀錄 ← 新增 */}
      {history.length > 0 && (
        <div className="card">
          <h3>🕐 最近查詢紀錄</h3>
          <div className="summary">
            {history.map((item, i) => (
              <div className="summary-row" key={i}>
                <span
                  style={{ cursor: "pointer", color: "#4f9cf9" }}
                  onClick={() => setSymbol(item.股票代號)}
                >
                  {item.股票代號}
                </span>
                <span>{item.公司名稱}</span>
                <span>{item.查詢時間.slice(0, 16)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 查詢結果 */}
      {stockData && (
        <>
          <StockCard
            info={stockData.基本資訊}
            summary={stockData.統計摘要}
          />

          {historyData.length > 0 && <StockChart data={historyData} />}

          {/* AI 分析按鈕 */}
          <button
            className="ai-btn"
            onClick={handleAiAnalysis}
            disabled={aiLoading}
          >
            {aiLoading ? "⏳ AI 分析中..." : "🤖 請 AI 分析這支股票"}
          </button>

          {/* AI 分析結果 */}
          {aiAnalysis && (
            <div className="card ai-result">
              <h3>🤖 AI 分析報告</h3>
              <pre>{aiAnalysis}</pre>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default App