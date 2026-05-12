// src/components/AssetPieChart.tsx

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { Portfolio } from "../types";

interface Props {
  portfolio: Portfolio;
}

const COLORS = ["#4f9cf9", "#51cf66", "#f9a84f", "#ff6b6b", "#c084fc"];

export default function AssetPieChart({ portfolio }: Props) {
  const data = portfolio.holdings.map((h) => ({
    name: h.symbol,
    value: h.value,
  }));

  return (
    <div className="card" style={{ marginBottom: 24 }}>
      <h2 style={{ marginBottom: 16 }}>資產分配</h2>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={100}
            dataKey="value"
            label={({ name, percent }) =>
              `${name} ${((percent ?? 0) * 100).toFixed(1)}%`
            }
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
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
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
