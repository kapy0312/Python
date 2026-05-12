// src/pages/Investments.tsx

import { useEffect, useState } from "react";
import { getPortfolio, createInvestment, deleteInvestment } from "../api";
import type { Portfolio } from "../types";

export default function Investments() {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState<{
    type: "tw_stock" | "us_stock" | "crypto";
    symbol: string;
    name: string;
    shares: string;
    cost_price: string;
  }>({
    type: "tw_stock",
    symbol: "",
    name: "",
    shares: "",
    cost_price: "",
  });

  async function fetchData() {
    const data = await getPortfolio();
    setPortfolio(data);
    setLoading(false);
  }

  useEffect(() => {
    fetchData();
  }, []);

  async function handleSubmit() {
    if (!form.symbol || !form.name || !form.shares || !form.cost_price) return;
    await createInvestment({
      type: form.type,
      symbol: form.symbol.toUpperCase(),
      name: form.name,
      shares: Number(form.shares),
      cost_price: Number(form.cost_price),
    });
    setForm({
      type: "tw_stock",
      symbol: "",
      name: "",
      shares: "",
      cost_price: "",
    });
    fetchData();
  }

  async function handleDelete(id: number) {
    await deleteInvestment(id);
    fetchData();
  }

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="page">
      <h1>📈 投資持倉</h1>

      {/* 新增表單 */}
      <div className="card" style={{ marginBottom: 24 }}>
        <h2 style={{ marginBottom: 16 }}>新增持倉</h2>
        <div className="form-grid">
          <select
            value={form.type}
            onChange={(e) =>
              setForm({
                ...form,
                type: e.target.value as "tw_stock" | "us_stock" | "crypto",
              })
            }
          >
            <option value="tw_stock">🇹🇼 台股</option>
            <option value="us_stock">🇺🇸 美股</option>
            <option value="crypto">🪙 加密貨幣</option>
          </select>

          <input
            type="text"
            placeholder="股票代號（如 2330.TW、AAPL、bitcoin）"
            value={form.symbol}
            onChange={(e) => setForm({ ...form, symbol: e.target.value })}
          />

          <input
            type="text"
            placeholder="名稱（如 台積電）"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />

          <input
            type="number"
            placeholder="持有數量"
            value={form.shares}
            onChange={(e) => setForm({ ...form, shares: e.target.value })}
          />

          <input
            type="number"
            placeholder="成本價"
            value={form.cost_price}
            onChange={(e) => setForm({ ...form, cost_price: e.target.value })}
          />
        </div>
        <button className="btn-primary" onClick={handleSubmit}>
          新增
        </button>
      </div>

      {/* 投資總覽 */}
      <div className="grid-3" style={{ marginBottom: 24 }}>
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

      {/* 持倉明細 */}
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>類型</th>
              <th>代號</th>
              <th>名稱</th>
              <th>持股數</th>
              <th>成本價</th>
              <th>現價</th>
              <th>成本（台幣）</th>
              <th>市值（台幣）</th>
              <th>損益（台幣）</th>
              <th>損益%</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {portfolio?.holdings.map((h) => (
              <tr key={h.id}>
                <td>
                  {h.type === "tw_stock" && "🇹🇼 台股"}
                  {h.type === "us_stock" && "🇺🇸 美股"}
                  {h.type === "crypto" && "🪙 加密貨幣"}
                </td>
                <td>{h.symbol}</td>
                <td>{h.name}</td>
                <td>{h.shares}</td>
                <td>
                  ${h.cost_price.toLocaleString()}
                  {h.usd_rate && (
                    <small style={{ color: "#64748b" }}>
                      {" "}
                      (${h.cost_price_twd.toLocaleString()} TWD)
                    </small>
                  )}
                </td>
                <td>
                  ${h.current_price.toLocaleString()}
                  {h.usd_rate && (
                    <small style={{ color: "#64748b" }}>
                      {" "}
                      (${h.current_price_twd.toLocaleString()} TWD)
                    </small>
                  )}
                </td>
                <td>${h.cost.toLocaleString()}</td>
                <td>${h.value.toLocaleString()}</td>
                <td className={h.profit >= 0 ? "income" : "expense"}>
                  ${h.profit.toLocaleString()}
                </td>
                <td className={h.profit_pct >= 0 ? "income" : "expense"}>
                  {h.profit_pct}%
                </td>
                <td>
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(h.id)}
                  >
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* 即時匯率 */}
        {portfolio?.usd_rate && (
          <div style={{ color: "#64748b", fontSize: 13, marginBottom: 16 }}>
            💱 即時匯率：1 USD = {portfolio.usd_rate} TWD
          </div>
        )}
      </div>
    </div>
  );
}
