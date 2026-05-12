// src/types/index.ts

export interface Category {
    id: number
    name: string
    type: "income" | "expense"
}

export interface Transaction {
    id: number
    category: number
    category_name: string
    amount: number
    note: string
    date: string
    created_at: string
}

export interface Investment {
    id: number
    type: "tw_stock" | "us_stock" | "crypto"
    symbol: string
    name: string
    shares: number
    cost_price: number
}

export interface Holding {
  id: number
  type: string
  symbol: string
  name: string
  shares: number
  cost_price: number
  cost_price_twd: number        // ← 加這行
  current_price: number
  current_price_twd: number     // ← 加這行
  usd_rate: number | null       // ← 加這行
  cost: number
  value: number
  profit: number
  profit_pct: number
}

export interface Portfolio {
    usd_rate: number       // ← 加這行
    holdings: Holding[]
    total_cost: number
    total_value: number
    total_profit: number
    total_profit_pct: number
}

export interface MonthlySummary {
    year: number
    month: number
    income: number
    expense: number
    balance: number
    by_category: {
        category: string
        total: number
    }[]
}

export interface Overview {
    year: number
    annual_income: number
    annual_expense: number
    annual_balance: number
    total_investment_cost: number
    total_investment_value: number
    total_investment_profit: number
    net_worth: number
}