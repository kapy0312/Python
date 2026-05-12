# tracker/admin.py

from django.contrib import admin
from .models import Category, Transaction, Investment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]
    list_filter  = ["type"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date", "category", "amount", "note"]
    list_filter  = ["category", "date"]
    ordering     = ["-date"]


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ["symbol", "name", "type", "shares", "cost_price"]
    list_filter  = ["type"]