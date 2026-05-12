# tracker/models.py

from django.db import models


# ── 分類（飲食、交通、薪資...）──────────────
class Category(models.Model):
    TYPES = [
        ("income", "收入"),
        ("expense", "支出"),
    ]
    name = models.CharField(max_length=50)        # 分類名稱
    type = models.CharField(max_length=10, choices=TYPES)  # 收入或支出

    def __str__(self):
        return f"{self.name}（{self.get_type_display()}）"


# ── 收支記錄 ──────────────────────────────────
class Transaction(models.Model):
    category   = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount     = models.DecimalField(max_digits=12, decimal_places=2)  # 金額
    note       = models.TextField(blank=True)      # 備註
    date       = models.DateField()                # 日期
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} {self.category} {self.amount}"


# ── 投資持倉 ──────────────────────────────────
class Investment(models.Model):
    TYPES = [
        ("tw_stock", "台股"),
        ("us_stock", "美股"),
        ("crypto",   "加密貨幣"),
    ]
    type       = models.CharField(max_length=20, choices=TYPES)
    symbol     = models.CharField(max_length=20)   # 股票代號 / 幣種
    name       = models.CharField(max_length=100)  # 公司名稱 / 幣名
    shares     = models.DecimalField(max_digits=20, decimal_places=6)  # 持有數量
    cost_price = models.DecimalField(max_digits=20, decimal_places=6)  # 成本價
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol}（{self.get_type_display()}）"