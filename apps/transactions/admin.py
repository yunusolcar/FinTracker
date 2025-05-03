from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "created_at", "updated_at"]
    list_filter = ["user"]
    search_fields = ["name", "user__email"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "amount",
        "transaction_type",
        "category",
        "user",
        "date",
    ]
    list_filter = ["transaction_type", "category", "user", "date"]
    search_fields = ["description", "user__email"]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["category", "amount", "user", "start_date", "end_date"]
    list_filter = ["category", "user", "start_date", "end_date"]
    search_fields = ["category__name", "user__email"]
