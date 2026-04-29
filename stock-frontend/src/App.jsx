import { useState } from "react"
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