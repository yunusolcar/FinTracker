from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Category(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    CATEGORY_TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name", "type")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.type})"

    def clean(self):
        if self.type not in [self.INCOME, self.EXPENSE]:
            raise ValidationError("Type must be either 'income' or 'expense'")

    def validate_name(self):
        if not self.name.strip():
            raise ValidationError("Name cannot be empty or contain only whitespace")
