// src/pages/Dashboard.tsx

import { useEffect, useState } from "react";
import { getOverview, getMonthlySummary, getPortfolio } from "../api";
import type { Overview, MonthlySummary, Portfolio } from "../types";
import MonthlyChart from "../components/MonthlyChart";
import AssetPieChart from "../components/AssetPieChart";

export default function Dashboard() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [summary, setSummary] = useState<MonthlySummary | null>(null);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);

  const now = new Date();

  useEffect(() => {
    Promise.all([
      getOverview(),
      getMonthlySummary(now.getFullYear(), now.getMonth() + 1),
      getPortfolio(),
    ]).then(([ov, sm, pf]) => {
      setOverview(ov);
      setSummary(sm);
      setPortfolio(pf);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="page">
      <h1>📊 資產總覽</h1>

      {/* 淨資產 */}
      <div className="card highlight">
        <span className="label">總淨資產</span>
        <span className="big-number">
          ${overview?.net_worth.toLocaleString()}
        </span>
      </div>

      {/* 本月收支 */}
      <h2>本月收支</h2>
      <div className="grid-3">
        <div className="card">
          <span className="label">本月收入</span>
          <span className="value income">
            +${summary?.income.toLocaleString()}
          </span>
        </div>
        <div className="card">
          <span className="label">本月支出</span>
          <span className="value expense">
            -${summary?.expense.toLocaleString()}
          </span>
        </div>
        <div className="card">
          <span className="label">本月結餘</span>
          <span
            className={`value ${
              (summary?.balance ?? 0) >= 0 ? "income" : "expense"
            }`}
          >
            ${summary?.balance.toLocaleString()}
          </span>
        </div>
      </div>

      {/* 投資損益 */}
      <h2>投資損益</h2>
      <div className="grid-3">
        <div className="card">
          <span className="label">投資成本</span>
          <span className="value">
            ${portfolio?.total_cost.toLocaleString()}
          </span>
        </div>
        <div className="card">
          <span className="label">目前市值</span>
          <span className="value">
            ${portfolio?.total_value.toLocaleString()}
          </span>
        </div>
        <div className="card">
          <span className="label">總損益</span>
          <span
            className={`value ${
              (portfolio?.total_profit ?? 0) >= 0 ? "income" : "expense"
            }`}
          >
            ${portfolio?.total_profit.toLocaleString()}
            <small> ({portfolio?.total_profit_pct}%)</small>
          </span>
        </div>
      </div>

      {/* 圖表區 */}
      <MonthlyChart />
      {portfolio && <AssetPieChart portfolio={portfolio} />}

      {/* 持倉明細 */}
      <h2>持倉明細</h2>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>代號</th>
              <th>名稱</th>
              <th>類型</th>
              <th>持股數</th>
              <th>成本價</th>
              <th>現價</th>
              <th>損益</th>
              <th>損益%</th>
            </tr>
          </thead>
          <tbody>
            {portfolio?.holdings.map((h) => (
              <tr key={h.id}>
                <td>{h.symbol}</td>
                <td>{h.name}</td>
                <td>
                  {h.type === "tw_stock"
                    ? "台股"
                    : h.type === "us_stock"
                    ? "美股"
                    : "加密貨幣"}
                </td>
                <td>{h.shares}</td>
                <td>${h.cost_price}</td>
                <td>${h.current_price}</td>
                <td className={h.profit >= 0 ? "income" : "expense"}>
                  ${h.profit.toLocaleString()}
                </td>
                <td className={h.profit_pct >= 0 ? "income" : "expense"}>
                  {h.profit_pct}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
