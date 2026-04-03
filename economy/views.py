from rest_framework import viewsets, permissions
from .models import FuelBalance, Transaction, RewardPool
from .serializers import FuelBalanceSerializer, TransactionSerializer, RewardPoolSerializer

class FuelBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FuelBalance.objects.all()
    serializer_class = FuelBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class RewardPoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RewardPool.objects.all()
    serializer_class = RewardPoolSerializer
