from rest_framework import viewsets

from network_node.models import NetworkNode


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """Вьюсет"""

    queryset = NetworkNode.objects.all()
