// src/components/MonthlyChart.tsx

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { useEffect, useState } from "react";
import { getMonthlySummary } from "../api";
import type { MonthlySummary } from "../types";

export default function MonthlyChart() {
  const [data, setData] = useState<MonthlySummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 抓最近 6 個月的資料
    const now = new Date();
    const promises = [];

    for (let i = 5; i >= 0; i--) {
      const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
      promises.push(getMonthlySummary(d.getFullYear(), d.getMonth() + 1));
    }

    Promise.all(promises).then((results) => {
      setData(results);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="loading">載入中...</div>;

  const chartData = data.map((d) => ({
    name: `${d.month}月`,
    收入: d.income,
    支出: d.expense,
    結餘: d.balance,
  }));

  return (
    <div className="card" style={{ marginBottom: 24 }}>
      <h2 style={{ marginBottom: 16 }}>近 6 個月收支</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2d3148" />
          <XAxis dataKey="name" tick={{ fontSize: 12, fill: "#94a3b8" }} />
          <YAxis
            tick={{ fontSize: 12, fill: "#94a3b8" }}
            tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
          />
          <Tooltip
            contentStyle={{
              background: "#1a1d2e",
              border: "1px solid #2d3148",
            }}
            formatter={(value: number | string | undefined) => [
              `$${Number(value ?? 0).toLocaleString()}`,
              "",
            ]}
          />
          <Legend />
          <Bar dataKey="收入" fill="#51cf66" radius={[4, 4, 0, 0]} />
          <Bar dataKey="支出" fill="#ff6b6b" radius={[4, 4, 0, 0]} />
          <Bar dataKey="結餘" fill="#4f9cf9" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
