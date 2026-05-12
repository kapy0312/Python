// src/pages/Transactions.tsx

import { useEffect, useState } from "react";
import {
  getTransactions,
  getCategories,
  createTransaction,
  deleteTransaction,
} from "../api";
import type { Transaction, Category } from "../types";

export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  // 新增表單
  const [form, setForm] = useState({
    category: "",
    amount: "",
    note: "",
    date: new Date().toISOString().slice(0, 10),
  });

  useEffect(() => {
    Promise.all([getTransactions(), getCategories()]).then(([tx, cat]) => {
      setTransactions(tx);
      setCategories(cat);
      setLoading(false);
    });
  }, []);

  async function handleSubmit() {
    if (!form.category || !form.amount || !form.date) return;
    await createTransaction({
      category: Number(form.category),
      amount: Number(form.amount),
      note: form.note,
      date: form.date,
    });
    // 重新拉取資料
    const tx = await getTransactions();
    setTransactions(tx);
    setForm({
      category: "",
      amount: "",
      note: "",
      date: new Date().toISOString().slice(0, 10),
    });
  }

  async function handleDelete(id: number) {
    await deleteTransaction(id);
    setTransactions((prev) => prev.filter((t) => t.id !== id));
  }

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="page">
      <h1>💰 收支記錄</h1>

      {/* 新增表單 */}
      <div className="card" style={{ marginBottom: 24 }}>
        <h2 style={{ marginBottom: 16 }}>新增記錄</h2>
        <div className="form-grid">
          <select
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value })}
          >
            <option value="">選擇分類</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}（{cat.type === "income" ? "收入" : "支出"}）
              </option>
            ))}
          </select>

          <input
            type="number"
            placeholder="金額"
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: e.target.value })}
          />

          <input
            type="date"
            value={form.date}
            onChange={(e) => setForm({ ...form, date: e.target.value })}
          />

          <input
            type="text"
            placeholder="備註（選填）"
            value={form.note}
            onChange={(e) => setForm({ ...form, note: e.target.value })}
          />
        </div>
        <button className="btn-primary" onClick={handleSubmit}>
          新增
        </button>
      </div>

      {/* 收支列表 */}
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>日期</th>
              <th>分類</th>
              <th>金額</th>
              <th>備註</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id}>
                <td>{t.date}</td>
                <td>{t.category_name}</td>
                <td
                  className={
                    categories.find((c) => c.id === t.category)?.type ===
                    "income"
                      ? "income"
                      : "expense"
                  }
                >
                  ${Number(t.amount).toLocaleString()}
                </td>
                <td>{t.note || "-"}</td>
                <td>
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(t.id)}
                  >
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
