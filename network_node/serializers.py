from rest_framework import serializers

from network_node.models import NetworkNode


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор модели поставщика: запрещает обновление поля Задолженность перед поставщиком через API"""
    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ("debt",)
