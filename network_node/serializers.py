from rest_framework import serializers

from network_node.models import Address, NetworkNode, Product


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
    """
    Сериализатор модели Поставщик:
    запрещает обновление поля Задолженность перед поставщиком через API
    """

    supplier = SupplierShortSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(), source="supplier", write_only=True, required=False
    )
    address = AddressShortSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source="address", write_only=True, required=False
    )

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "email",
            "supplier",
            "supplier_id",
            "address",
            "address_id",
            "debt",
            "level",
            "created_at",
        )
        read_only_fields = ("debt",)


class NetworkNodeDetailSerializer(NetworkNodeListSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta(NetworkNodeListSerializer.Meta):
        fields = NetworkNodeListSerializer.Meta.fields + ("products",)
