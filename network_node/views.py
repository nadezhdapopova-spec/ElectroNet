from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from network_node.models import NetworkNode
from network_node.permissions import IsActiveEmployee
from network_node.serializers import NetworkNodeDetailSerializer, NetworkNodeListSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Поставщик"""

    queryset = NetworkNode.objects.select_related("address", "supplier").prefetch_related("products").order_by("id")
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["level", "address__country", "address__city"]

    def get_serializer_class(self):
        """
        list-эндпоинт: общая информация об объекте сети.
        detail-эндпоинт: дополнительно выводится список товаров
        """
        if self.action == "retrieve":
            return NetworkNodeDetailSerializer
        return NetworkNodeListSerializer
