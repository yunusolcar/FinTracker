from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import re

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Category name can only contain letters, numbers and spaces
        if not all(c.isalnum() or c.isspace() for c in self.name):
            raise ValidationError(
                _("Category name can only contain letters, numbers and spaces.")
            )

        # Category name cannot be empty or only spaces
        if not self.name.strip():
            raise ValidationError(_("Category name cannot be empty."))

        # Category name length check
        if len(self.name.strip()) < 2:
            raise ValidationError(
                _("Category name must be at least 2 characters long.")
            )

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ["name", "user"]  # Unique category names per user


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="transactions"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message="Amount cannot be less than 0.01"),
            MaxValueValidator(
                1000000, message="Amount cannot be greater than 1,000,000"
            ),
        ],
    )
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.category.name}"

    def clean(self):
        # Description sanitization
        if self.description:
            # Remove HTML tags
            self.description = re.sub(r"<[^>]+>", "", self.description)

            # Remove potentially dangerous characters
            self.description = re.sub(r"[<>{}[\]]", "", self.description)

            # Remove multiple spaces
            self.description = re.sub(r"\s+", " ", self.description).strip()

            # Truncate if too long
            if len(self.description) > 255:
                self.description = self.description[:252] + "..."

            # Check for special characters
            if not all(c.isprintable() for c in self.description):
                raise ValidationError(_("Invalid characters in the description."))

        # Date cannot be in the future
        if self.date > timezone.now().date():
            raise ValidationError(_("Transaction date cannot be in the future."))

        # Check if category belongs to user
        if self.category.user != self.user:
            raise ValidationError(_("This category does not belong to you."))

    def save(self, *args, **kwargs):
        self.full_clean()  # Run model validations
        super().save(*args, **kwargs)


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="budgets"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(1000000),  # maximum 1 million
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"

    def clean(self):
        # Date check
        if self.end_date <= self.start_date:
            raise ValidationError(_("End date must be after start date."))

        # Check for overlapping budgets
        overlapping_budgets = Budget.objects.filter(
            user=self.user,
            category=self.category,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(pk=self.pk if self.pk else None)

        if overlapping_budgets.exists():
            raise ValidationError(_("This date range already has a budget."))

    def save(self, *args, **kwargs):
        self.full_clean()  # Run model validations
        super().save(*args, **kwargs)
