from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network_node.models import NetworkNode, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Админ-панель для отображения объектов сети"""
    list_display = ("name", "city", "supplier", "debt", "created_at")
    list_filter = ("city", "country")
    readonly_fields = ("supplier_link",)
    inlines = [ProductInline]

    def supplier_link(self, obj):
        """Отображает ссылку на поставщика на странице объекта"""
        if obj.supplier:
            url = reverse("admin:network_node_networknode_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    @admin.action(description="Очистить задолженность")
    def clear_debt(modeladmin, request, queryset):
        """Очищает задолженность перед поставщиком у выбранных объектов"""
        queryset.update(debt=0)

    actions = [clear_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для отображения продуктов"""
    list_display = ("name", "model", "release_date", "node")
    list_filter = ("release_date",)
