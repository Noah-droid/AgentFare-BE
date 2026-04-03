from rest_framework import viewsets, mixins
from .models import WorldEvent
from .serializers import WorldEventSerializer

class WorldEventViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Read-only view for the drama feed.
    """
    queryset = WorldEvent.objects.all()
    serializer_class = WorldEventSerializer
    filterset_fields = ['world', 'agent', 'severity', 'event_type']

    def get_queryset(self):
        queryset = super().get_queryset()
        world_id = self.request.query_params.get('world_id')
        if world_id:
            queryset = queryset.filter(world_id=world_id)
        return queryset
