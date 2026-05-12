# tracker/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from datetime import datetime, date
from .models import Category, Transaction, Investment
from .serializers import CategorySerializer, TransactionSerializer, InvestmentSerializer
from .price_fetcher import get_price, get_usd_to_twd


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-date")
    serializer_class = TransactionSerializer

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """
        月收支統計
        GET /api/transactions/summary/?year=2026&month=5
        """
        year = int(request.query_params.get("year",  datetime.now().year))
        month = int(request.query_params.get("month", datetime.now().month))

        transactions = Transaction.objects.filter(
            date__year=year,
            date__month=month
        )

        income = transactions.filter(category__type="income").aggregate(
            total=Sum("amount"))["total"] or 0
        expense = transactions.filter(category__type="expense").aggregate(
            total=Sum("amount"))["total"] or 0

        # 每個分類的支出明細
        by_category = []
        categories = Category.objects.filter(type="expense")
        for cat in categories:
            total = transactions.filter(category=cat).aggregate(
                total=Sum("amount"))["total"] or 0
            if total > 0:
                by_category.append({
                    "category": cat.name,
                    "total":    float(total),
                })

        return Response({
            "year":        year,
            "month":       month,
            "income":      float(income),
            "expense":     float(expense),
            "balance":     float(income - expense),
            "by_category": by_category,
        })


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

    @action(detail=False, methods=["get"])
    def portfolio(self, request):
        """
        投資損益總覽
        GET /api/investments/portfolio/
        """
        investments = Investment.objects.all()
        result = []
        total_cost = 0
        total_value = 0
        usd_rate = get_usd_to_twd()  # ← 抓一次匯率

        for inv in investments:
            current_price = get_price(inv.type, inv.symbol)

            # 美股和加密貨幣需要換算成台幣
            if inv.type in ["us_stock", "crypto"]:
                current_price_twd = current_price * usd_rate
                cost_price_twd = float(inv.cost_price) * usd_rate
            else:
                current_price_twd = current_price
                cost_price_twd = float(inv.cost_price)

            cost = float(inv.shares) * cost_price_twd
            value = float(inv.shares) * current_price_twd
            profit = value - cost
            profit_pct = (profit / cost * 100) if cost > 0 else 0

            total_cost += cost
            total_value += value

            result.append({
                "id":            inv.id,
                "type":          inv.type,
                "symbol":        inv.symbol,
                "name":          inv.name,
                "shares":        float(inv.shares),
                "cost_price":    float(inv.cost_price),
                "cost_price_twd": round(cost_price_twd, 2),
                "current_price": current_price,
                "current_price_twd": round(current_price_twd, 2),
                "usd_rate":      usd_rate if inv.type in ["us_stock", "crypto"] else None,
                "cost":          round(cost, 2),
                "value":         round(value, 2),
                "profit":        round(profit, 2),
                "profit_pct":    round(profit_pct, 2),
            })

        return Response({
            "usd_rate":         usd_rate,
            "holdings":         result,
            "total_cost":       round(total_cost, 2),
            "total_value":      round(total_value, 2),
            "total_profit":     round(total_value - total_cost, 2),
            "total_profit_pct": round((total_value - total_cost) / total_cost * 100, 2) if total_cost > 0 else 0,
        })

    @action(detail=False, methods=["get"])
    def overview(self, request):
        """
        資產總覽
        GET /api/investments/overview/
        """
        # 計算今年總收入、總支出
        year = datetime.now().year
        income = Transaction.objects.filter(
            date__year=year, category__type="income"
        ).aggregate(total=Sum("amount"))["total"] or 0

        expense = Transaction.objects.filter(
            date__year=year, category__type="expense"
        ).aggregate(total=Sum("amount"))["total"] or 0

        # 計算投資總值
        investments = Investment.objects.all()
        usd_rate = get_usd_to_twd()   # ← 加這行
        total_investment_cost = 0
        total_investment_value = 0

        for inv in investments:
            current_price = get_price(inv.type, inv.symbol)

            # ← 加匯率換算
            if inv.type in ["us_stock", "crypto"]:
                current_price_twd = current_price * usd_rate
                cost_price_twd = float(inv.cost_price) * usd_rate
            else:
                current_price_twd = current_price
                cost_price_twd = float(inv.cost_price)

            cost = float(inv.shares) * cost_price_twd
            value = float(inv.shares) * current_price_twd
            total_investment_cost += cost
            total_investment_value += value

        investment_profit = total_investment_value - total_investment_cost

        return Response({
            "year":                    year,
            "annual_income":           float(income),
            "annual_expense":          float(expense),
            "annual_balance":          float(income - expense),
            "usd_rate":                usd_rate,
            "total_investment_cost":   round(total_investment_cost, 2),
            "total_investment_value":  round(total_investment_value, 2),
            "total_investment_profit": round(investment_profit, 2),
            "net_worth":               round(float(income - expense) + total_investment_value, 2),
        })
