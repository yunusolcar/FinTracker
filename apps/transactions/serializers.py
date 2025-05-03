from rest_framework import serializers
from .models import Category, Transaction, Budget


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        # Add user information
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


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
            raise serializers.ValidationError("Amount must be greater than 0.")
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
