from django.urls import path, include
from orders.api.v1.viewsets import OrderViewSet
from rest_framework.routers import DefaultRouter


app_name = "v1"
router = DefaultRouter()

router.register(r'orders', OrderViewSet, basename='orders')

v1_urlpatterns = [
    path('v1/', include(router.urls)),
]
