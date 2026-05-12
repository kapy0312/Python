// src/App.tsx

import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Investments from "./pages/Investments";
import "./App.css";

type Page = "dashboard" | "transactions" | "investments";

function App() {
  const [page, setPage] = useState<Page>("dashboard");

  return (
    <div className="app">
      <nav className="nav">
        <span className="nav-brand">💼 記帳系統</span>
        <div className="nav-links">
          <button
            className={page === "dashboard" ? "nav-btn active" : "nav-btn"}
            onClick={() => setPage("dashboard")}
          >
            總覽
          </button>
          <button
            className={page === "transactions" ? "nav-btn active" : "nav-btn"}
            onClick={() => setPage("transactions")}
          >
            收支記錄
          </button>
          <button
            className={page === "investments" ? "nav-btn active" : "nav-btn"}
            onClick={() => setPage("investments")}
          >
            投資持倉
          </button>
        </div>
      </nav>

      {page === "dashboard" && <Dashboard />}
      {page === "transactions" && <Transactions />}
      {page === "investments" && <Investments />}
    </div>
  );
}

export default App;
