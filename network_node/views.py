from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from network_node.models import NetworkNode
from network_node.permissions import IsActiveEmployee
from network_node.serializers import NetworkNodeDetailSerializer, NetworkNodeListSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели поставщика"""
    queryset = NetworkNode.objects.select_related("address", "supplier").prefetch_related("products")
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["level", "address__country", "address__city"]

    def get_serializer_class(self):
        """
        API List(/api/nodes/): общая информация об объекте сети.
        API Detail(/api/nodes/1/): дополнительно выводится список товаров
        """
        if self.action == "retrieve":
            return NetworkNodeDetailSerializer
        return NetworkNodeListSerializer
