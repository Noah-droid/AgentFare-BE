from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import World, ResourceNode
from .serializers import WorldSerializer, ResourceNodeSerializer
from agents.models import Agent

class WorldViewSet(viewsets.ModelViewSet):
    queryset = World.objects.all()
    serializer_class = WorldSerializer

    @action(detail=True, methods=['get'])
    def map_state(self, request, pk=None):
        world = self.get_object()
        agents = world.agents.filter(status=Agent.Status.ACTIVE).values(
            'id', 'persona', 'position_x', 'position_y', 'energy', 'wealth'
        )
        resources = world.resource_nodes.all().values(
            'id', 'resource_type', 'position_x', 'position_y', 'quantity'
        )
        return Response({
            'current_tick': world.current_tick,
            'agents': list(agents),
            'resources': list(resources)
        })

    @action(detail=True, methods=['post'])
    def start_season(self, request, pk=None):
        world = self.get_object()
        world.status = World.Status.ENTRY
        world.save()
        return Response({'status': 'season started'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def close_entry(self, request, pk=None):
        world = self.get_object()
        world.status = World.Status.ACTIVE
        world.save()
        return Response({'status': 'entry window closed'}, status=status.HTTP_200_OK)

class ResourceNodeViewSet(viewsets.ModelViewSet):
    queryset = ResourceNode.objects.all()
    serializer_class = ResourceNodeSerializer
