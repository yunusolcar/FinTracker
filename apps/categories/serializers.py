from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type", "description", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        request = self.context.get("request")
        if request and request.method == "POST":
            if Category.objects.filter(
                user=request.user, name=data["name"], type=data["type"]
            ).exists():
                raise serializers.ValidationError(
                    "A category with this name and type already exists for your account."
                )
        return data
