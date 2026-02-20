from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network_node.models import Address, NetworkNode, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("country", "city", "street", "house_number")
    search_fields = ("country", "city", "street")


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Админ-панель для отображения объектов сети"""

    list_display = ("name", "get_country", "get_city", "supplier", "debt", "level", "created_at")
    list_filter = ("level", "address__city", "address__country")
    autocomplete_fields = ("address", "supplier")
    readonly_fields = ("supplier_link", "level")
    inlines = [ProductInline]
    search_fields = ("name", "email")

    def supplier_link(self, obj):
        """Отображает ссылку на поставщика на странице объекта"""
        if obj.supplier:
            url = reverse("admin:network_node_networknode_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def get_country(self, obj):
        return obj.address.country

    get_country.short_description = "Country"

    def get_city(self, obj):
        return obj.address.city

    get_city.short_description = "City"

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
