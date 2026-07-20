from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.api.v1.viewsets import OrderViewSet as OrderViewSetV1
from payments.api.v1.viewsets import PaymentViewSet as PaymentViewSetV1


router = DefaultRouter()

router.register(r'orders', OrderViewSetV1, basename='orders')
router.register(r'payments', PaymentViewSetV1, basename='payments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
