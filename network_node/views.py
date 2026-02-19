from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from network_node.models import NetworkNode
from network_node.permissions import IsActiveEmployee
from network_node.serializers import NetworkNodeSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели поставщика"""

    queryset = NetworkNode.objects.select_related("supplier")
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]
