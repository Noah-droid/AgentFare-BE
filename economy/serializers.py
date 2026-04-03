from rest_framework import serializers
from .models import FuelBalance, Transaction, RewardPool

class FuelBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelBalance
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class RewardPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardPool
        fields = '__all__'
