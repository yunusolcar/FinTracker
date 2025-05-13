from rest_framework import serializers
from django.utils import timezone
from .models import Category, Transaction, Budget
import re


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        # Add user information to validated data
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate_name(self, value):
        # Check for duplicate category names (case insensitive)
        if Category.objects.filter(
            user=self.context["request"].user, name__iexact=value.strip()
        ).exists():
            raise serializers.ValidationError(
                "A category with this name already exists."
            )
        return value.strip()


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "description",
            "transaction_type",
            "date",
            "category",
            "category_name",
            "is_recurring",
            "recurring_type",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "category_name",
        ]

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description cannot be empty.")

        # Remove HTML tags
        value = re.sub(r"<[^>]+>", "", value)

        # Remove potentially dangerous characters
        value = re.sub(r"[<>{}[\]]", "", value)

        # Remove multiple spaces
        value = re.sub(r"\s+", " ", value).strip()

        # Check minimum length
        if len(value) < 3:
            raise serializers.ValidationError(
                "Description must be at least 3 characters long."
            )

        # Check for special characters
        if not all(c.isprintable() for c in value):
            raise serializers.ValidationError(
                "Description contains invalid characters."
            )

        return value

    def create(self, validated_data):
        # Add user information
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate_category(self, value):
        # Check if the category belongs to the user
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("This category does not belong to you.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Transaction date cannot be in the future."
            )
        return value

    def validate_transaction_type(self, value):
        if value.lower() not in [
            choice[0] for choice in Transaction.TRANSACTION_TYPE_CHOICES
        ]:
            raise serializers.ValidationError("Invalid transaction type.")
        return value.lower()

    def validate_recurring_type(self, value):
        # Validate recurring type if present
        if (
            value
            and value != "none"
            and value not in [choice[0] for choice in Transaction.RECURRING_CHOICES]
        ):
            raise serializers.ValidationError("Invalid recurring type.")
        return value


class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Budget
        fields = [
            "id",
            "amount",
            "start_date",
            "end_date",
            "category",
            "category_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "category_name"]

    def create(self, validated_data):
        # Add user information
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate_category(self, value):
        # Check if the category belongs to the user
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("This category does not belong to you.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget amount must be greater than 0.")
        return value

    def validate(self, data):
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date.")

        # Check for overlapping budgets
        overlapping_budgets = Budget.objects.filter(
            user=self.context["request"].user,
            category=data["category"],
            start_date__lte=data["end_date"],
            end_date__gte=data["start_date"],
        ).exclude(pk=self.instance.pk if self.instance else None)

        if overlapping_budgets.exists():
            raise serializers.ValidationError(
                "A budget already exists for this date range."
            )

        return data
