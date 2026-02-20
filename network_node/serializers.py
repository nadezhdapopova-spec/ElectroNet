from rest_framework import serializers

from network_node.models import Address, NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор модели Товар: информация о продукте, связанном с конкретным звеном сети"""

    class Meta:
        model = Product
        fields = ("id", "name", "model", "release_date")


class AddressShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор адреса (address): контактная информация звена сети в списке и детальном представлении"""

    class Meta:
        model = Address
        fields = ("id", "country", "city", "street", "house_number")


class SupplierShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор поставщика (supplier): информация о связанномзвене сети (id, name, email)"""

    class Meta:
        model = NetworkNode
        fields = ("id", "name", "email")


class NetworkNodeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Поставщик для list-эндпоинта: информация о звене сети
    - Поле debt (Задолженность перед поставщиком) запрещено обновлять через API.
    - Поля supplier и address отображаются в виде вложенных объектов.
    - Для put/patch-эндпоинтов используются поля supplier_id и address_id
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
    """Сериализатор модели Поставщик для detail-эндпоинта: дополнительно включает список связанных продуктов"""

    products = ProductSerializer(many=True, read_only=True)

    class Meta(NetworkNodeListSerializer.Meta):
        fields = NetworkNodeListSerializer.Meta.fields + ("products",)
