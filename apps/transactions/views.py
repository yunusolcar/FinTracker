from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
from .models import Category, Transaction, Budget
from .serializers import CategorySerializer, TransactionSerializer, BudgetSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show only user's own categories
        return Category.objects.filter(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show only user's own transactions
        queryset = Transaction.objects.filter(user=self.request.user)

        # Filtering options
        category = self.request.query_params.get("category", None)
        transaction_type = self.request.query_params.get("type", None)
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        if category:
            queryset = queryset.filter(category__name=category)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Sorting
        sort_by = self.request.query_params.get("sort_by", "-date")
        return queryset.order_by(sort_by)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Transaction summary for a specific date range"""
        start_date = request.query_params.get(
            "start_date", timezone.now().replace(day=1).date()
        )
        end_date = request.query_params.get("end_date", timezone.now().date())

        # Calculate income and expense totals
        income = Transaction.objects.filter(
            user=request.user,
            transaction_type="income",
            date__range=[start_date, end_date],
        ).aggregate(total=Sum("amount"))

        expense = Transaction.objects.filter(
            user=request.user,
            transaction_type="expense",
            date__range=[start_date, end_date],
        ).aggregate(total=Sum("amount"))

        # Expense report by category
        expenses_by_category = (
            Transaction.objects.filter(
                user=request.user,
                transaction_type="expense",
                date__range=[start_date, end_date],
            )
            .values("category__name")
            .annotate(total=Sum("amount"))
        )

        return Response(
            {
                "start_date": start_date,
                "end_date": end_date,
                "total_income": income["total"] or 0,
                "total_expense": expense["total"] or 0,
                "balance": (income["total"] or 0) - (expense["total"] or 0),
                "expenses_by_category": expenses_by_category,
            }
        )


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show only user's own budgets
        return Budget.objects.filter(user=self.request.user)

    @action(detail=True, methods=["get"])
    def status(self, request, pk=None):
        """Check budget status"""
        budget = self.get_object()

        # Calculate expenses in budget category
        expenses = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            transaction_type="expense",
            date__range=[budget.start_date, budget.end_date],
        ).aggregate(total=Sum("amount"))

        total_spent = expenses["total"] or 0
        remaining = budget.amount - total_spent
        percentage_used = (
            (total_spent / budget.amount) * 100 if budget.amount > 0 else 0
        )

        return Response(
            {
                "budget_id": budget.id,
                "category": budget.category.name,
                "budget_amount": budget.amount,
                "total_spent": total_spent,
                "remaining": remaining,
                "percentage_used": percentage_used,
                "status": "warning" if percentage_used > 80 else "ok",
            }
        )
