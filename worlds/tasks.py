import logging
from celery import shared_task
from django.db import transaction
from worlds.models import World
from agents.models import Agent, SpawnQueue
from events.models import WorldEvent

logger = logging.getLogger(__name__)

@shared_task
def process_world_tick(world_id):
    """
    The main tick processing task for a specific world.
    """
    try:
        with transaction.atomic():
            world = World.objects.select_for_update().get(id=world_id)
            
            if world.status not in [World.Status.ENTRY, World.Status.ACTIVE, World.Status.ENDGAME]:
                logger.info(f"World {world_id} is in status {world.status}, skipping tick.")
                return

            world.current_tick += 1
            world.save()
            
            logger.info(f"Processing World {world_id} Tick {world.current_tick}")
            
            # 1. Spawn agents from queue if in entry window
            if world.status == World.Status.ENTRY:
                spawn_queued_agents(world)
            
            # 2. Trigger individual agent loops
            active_agents = Agent.objects.filter(world=world, status=Agent.Status.ACTIVE)
            for agent in active_agents:
                run_agent_loop.delay(agent.id, world.current_tick)
                
            # 3. Log tick event
            WorldEvent.objects.create(
                world=world,
                tick=world.current_tick,
                event_type="TICK_PROCESSED",
                description=f"World tick {world.current_tick} processed successfully."
            )
            
    except World.DoesNotExist:
        logger.error(f"World {world_id} does not exist.")
    except Exception as e:
        logger.exception(f"Error processing tick for world {world_id}: {e}")

@shared_task
def spawn_world_resources(world_id):
    """
    Initial population of resources for a new world.
    """
    import random
    from worlds.models import World, ResourceNode
    
    world = World.objects.get(id=world_id)
    resource_types = ['ENERGY_GLOW', 'WATER_VAPOR', 'SCRAP_METAL', 'BIO_FLOWER']
    
    for _ in range(50): # Spawn 50 nodes
        ResourceNode.objects.create(
            world=world,
            position_x=random.randint(0, world.map_size_x),
            position_y=random.randint(0, world.map_size_y),
            resource_type=random.choice(resource_types),
            quantity=random.randint(5, 20)
        )
    
    WorldEvent.objects.create(
        world=world,
        tick=world.current_tick,
        event_type="RESOURCES_SPAWNED",
        description="A fresh set of resources has been detected in the world."
    )

def spawn_queued_agents(world):
    """
    Spawns agents that are scheduled for the current tick.
    """
    queued_entries = SpawnQueue.objects.filter(world=world, spawn_tick__lte=world.current_tick)
    for entry in queued_entries:
        agent = entry.agent
        agent.status = Agent.Status.ACTIVE
        agent.world = world
        # Set initial position randomly or at spawn points
        agent.position_x = 50 
        agent.position_y = 50
        agent.save()
        
        WorldEvent.objects.create(
            world=world,
            tick=world.current_tick,
            agent=agent,
            event_type="AGENT_SPAWNED",
            description=f"Agent {agent.id} has entered the world."
        )
        entry.delete()

@shared_task
def run_agent_loop(agent_id, tick):
    """
    The individual agent's reasoning and action cycle.
    """
    from agents.tasks import execute_agent_cognition
    execute_agent_cognition.delay(agent_id, tick)
