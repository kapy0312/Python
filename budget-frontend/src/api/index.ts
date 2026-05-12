// src/api/index.ts

import axios from "axios"
import type {
  Category, Transaction, Investment,   // ← 加 Investment
  Portfolio, MonthlySummary, Overview
} from "../types"

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
})

export const getCategories = () =>
  API.get<Category[]>("/categories/").then(r => r.data)

export const getTransactions = () =>
  API.get<Transaction[]>("/transactions/").then(r => r.data)

export const createTransaction = (data: Partial<Transaction>) =>
  API.post<Transaction>("/transactions/", data).then(r => r.data)

export const deleteTransaction = (id: number) =>
  API.delete(`/transactions/${id}/`)

export const getPortfolio = () =>
  API.get<Portfolio>("/investments/portfolio/").then(r => r.data)

export const getMonthlySummary = (year: number, month: number) =>
  API.get<MonthlySummary>(`/transactions/summary/?year=${year}&month=${month}`).then(r => r.data)

export const getOverview = () =>
  API.get<Overview>("/investments/overview/").then(r => r.data)

export const createInvestment = (data: Partial<Investment>) =>
  API.post<Investment>("/investments/", data).then(r => r.data)

export const deleteInvestment = (id: number) =>
  API.delete(`/investments/${id}/`)