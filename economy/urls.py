from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FuelBalanceViewSet, TransactionViewSet, RewardPoolViewSet

router = DefaultRouter()
router.register(r'balance', FuelBalanceViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'rewards', RewardPoolViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
