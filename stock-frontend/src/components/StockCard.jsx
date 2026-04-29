function StockCard({ info, summary }) {
    return (
        <div className="card">
            <div className="card-header">
                <div>
                    <h2>{info.公司名稱}</h2>
                    <span className="symbol">{info.股票代號}</span>
                </div>
                <div className="price">${info.目前股價}</div>
            </div>

            {/* 基本指標 */}
            <div className="metrics">
                <div className="metric">
                    <span className="label">52週最高</span>
                    <span className="value">${info["52週最高"]}</span>
                </div>
                <div className="metric">
                    <span className="label">52週最低</span>
                    <span className="value">${info["52週最低"]}</span>
                </div>
                <div className="metric">
                    <span className="label">本益比</span>
                    <span className="value">
                        {info.本益比 !== "N/A" ? Number(info.本益比).toFixed(2) : "N/A"}
                    </span>
                </div>
                <div className="metric">
                    <span className="label">期間漲跌</span>
                    <span className={`value ${summary.期間漲跌幅.startsWith("+") ? "up" : "down"}`}>
                        {summary.期間漲跌幅}
                    </span>
                </div>
            </div>

            {/* 統計摘要 */}
            <div className="summary">
                <div className="summary-row">
                    <span>分析期間</span>
                    <span>{summary.分析期間}</span>
                </div>
                <div className="summary-row">
                    <span>起始收盤價</span>
                    <span>${summary.起始收盤價}</span>
                </div>
                <div className="summary-row">
                    <span>最新收盤價</span>
                    <span>${summary.最新收盤價}</span>
                </div>
                <div className="summary-row">
                    <span>期間最高價</span>
                    <span>${summary.期間最高價}</span>
                </div>
                <div className="summary-row">
                    <span>期間最低價</span>
                    <span>${summary.期間最低價}</span>
                </div>
                <div className="summary-row">
                    <span>平均成交量</span>
                    <span>{summary.平均成交量}</span>
                </div>
            </div>
        </div>
    )
}

export default StockCard