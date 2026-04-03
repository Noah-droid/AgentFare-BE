from rest_framework import serializers
from .models import World, ResourceNode

class WorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = '__all__'

class ResourceNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceNode
        fields = '__all__'
