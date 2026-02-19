from rest_framework import serializers

from network_node.models import NetworkNode, Product, Address


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "model", "release_date")


class AddressShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "country", "city", "street", "house_number")


class SupplierShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = ("id", "name", "email")


class NetworkNodeListSerializer(serializers.ModelSerializer):
    """Сериализатор модели поставщика: запрещает обновление поля Задолженность перед поставщиком через API"""
    supplier = SupplierShortSerializer(read_only=True)
    address = AddressShortSerializer(read_only=True)

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "email",
            "supplier",
            "address",
            "debt",
            "level",
            "created_at",
        )
        read_only_fields = ("debt",)


class NetworkNodeDetailSerializer(NetworkNodeListSerializer):
    products = ProductSerializer(many=True, read_only=True)
