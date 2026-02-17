from django.urls import include, path

from rest_framework.routers import DefaultRouter

from network_node.views import NetworkNodeViewSet

app_name = "network_node"

router = DefaultRouter()
router.register(r"nodes", NetworkNodeViewSet, basename="node")   # /api/nodes/ и для reverse("network_node:node-list") и node-detail

urlpatterns = [
    path("", include(router.urls)),
]
