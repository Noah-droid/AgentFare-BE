from rest_framework import serializers
from .models import Agent, SpawnQueue

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
        read_only_fields = ['owner', 'status', 'wealth', 'reputation', 'energy', 'hunger']

class SpawnQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpawnQueue
        fields = '__all__'
