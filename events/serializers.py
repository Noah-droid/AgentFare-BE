from rest_framework import serializers
from .models import WorldEvent

class WorldEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldEvent
        fields = '__all__'
