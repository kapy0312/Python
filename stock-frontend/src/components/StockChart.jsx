import {
    LineChart, Line, XAxis, YAxis,
    CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts"

function StockChart({ data }) {
    if (!data || data.length === 0) return null

    return (
        <div className="card">
            <h3>股價走勢圖</h3>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis
                        dataKey="日期"
                        tick={{ fontSize: 11 }}
                        tickFormatter={val => val.slice(5)}  // 只顯示 月-日
                    />
                    <YAxis
                        domain={["auto", "auto"]}
                        tick={{ fontSize: 11 }}
                        tickFormatter={val => `$${val}`}
                    />
                    <Tooltip
                        formatter={(value) => [`$${value}`, ""]}
                        labelFormatter={(label) => `日期：${label}`}
                    />
                    <Legend />
                    <Line type="monotone" dataKey="收盤" stroke="#4f9cf9" dot={false} strokeWidth={2} />
                    <Line type="monotone" dataKey="MA5" stroke="#f9a84f" dot={false} strokeWidth={1.5} strokeDasharray="4 2" />
                    <Line type="monotone" dataKey="MA20" stroke="#4ff9a8" dot={false} strokeWidth={1.5} strokeDasharray="4 2" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}

export default StockChart