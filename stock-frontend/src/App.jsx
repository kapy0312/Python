import { useState } from "react"
import StockCard from "./components/StockCard"
import StockChart from "./components/StockChart"
import "./App.css"

function App() {
  const [symbol, setSymbol] = useState("")      // 使用者輸入的股票代號
  const [period, setPeriod] = useState("3mo")   // 查詢期間
  const [stockData, setStockData] = useState(null)  // 基本資訊 + 統計摘要
  const [historyData, setHistoryData] = useState([]) // 歷史K線
  const [loading, setLoading] = useState(false)  // 載入中
  const [error, setError] = useState("")         // 錯誤訊息

  async function handleSearch() {
    if (!symbol.trim()) return

    setLoading(true)
    setError("")
    setStockData(null)
    setHistoryData([])

    try {
      // 同時發兩個請求
      const [infoRes, historyRes] = await Promise.all([
        fetch(`/stock/${symbol.trim().toUpperCase()}?period=${period}`),
        fetch(`/stock/${symbol.trim().toUpperCase()}/history?period=${period}`)
      ])

      if (!infoRes.ok) {
        throw new Error("找不到股票，請確認代號是否正確")
      }

      const infoData = await infoRes.json()
      const histData = await historyRes.json()

      setStockData(infoData)
      setHistoryData(histData.歷史資料 || [])

    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // 按 Enter 也能查詢
  function handleKeyDown(e) {
    if (e.key === "Enter") handleSearch()
  }

  return (
    <div className="container">
      <h1>📈 股票查詢系統</h1>

      {/* 搜尋區 */}
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
      {error && <div className="error">{error}</div>}

      {/* 查詢結果 */}
      {stockData && (
        <>
          <StockCard
            info={stockData.基本資訊}
            summary={stockData.統計摘要}
          />
          <StockChart data={historyData} />
        </>
      )}
    </div>
  )
}

export default App