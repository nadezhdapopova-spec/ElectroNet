from rest_framework import viewsets

from network_node.models import NetworkNode
from network_node.permissions import IsActiveEmployee


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели поставщика"""

    queryset = NetworkNode.objects.all()
    filterset_fields = ["country"]
    permission_classes = [IsActiveEmployee]
