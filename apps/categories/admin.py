from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "type", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("name", "description", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.user == request.user or request.user.is_superuser
