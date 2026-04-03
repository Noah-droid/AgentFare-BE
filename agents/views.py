from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Agent, SpawnQueue
from .serializers import AgentSerializer, SpawnQueueSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def join_world(self, request, pk=None):
        agent = self.get_object()
        world_id = request.data.get('world_id')
        fuel_commitment = request.data.get('fuel_commitment', 10.0) # Placeholder
        
        # 1. Validate world exists and status is CREATION or ENTRY
        from worlds.models import World
        try:
            world = World.objects.get(id=world_id)
            if world.status not in [World.Status.CREATION, World.Status.ENTRY]:
                return Response({'error': 'World not accepting new agents.'}, status=status.HTTP_400_BAD_REQUEST)
        except World.DoesNotExist:
            return Response({'error': 'World not found.'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Assign to world and queue for spawn
        import random
        spawn_tick = world.current_tick + random.randint(1, 5) # Random spawn within next 5 ticks
        
        agent.world = world
        agent.status = Agent.Status.QUEUED
        agent.save()
        
        SpawnQueue.objects.create(
            agent=agent,
            world=world,
            spawn_tick=spawn_tick
        )
        
        return Response({'status': 'agent queued', 'spawn_tick': spawn_tick}, status=status.HTTP_201_CREATED)
