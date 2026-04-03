import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from worlds.models import World
from agents.models import Agent, SpawnQueue

def bulk_spawn(count=10):
    user, _ = User.objects.get_or_create(username='admin')
    world = World.objects.get(season_number=1)
    
    personas = [p[0] for p in Agent.Persona.choices]
    tiers = [t[0] for t in Agent.IntelligenceTier.choices]
    
    for i in range(count):
        persona = random.choice(personas)
        tier = random.choice(tiers)
        
        agent = Agent.objects.create(
            owner=user,
            persona=persona,
            intelligence_tier=tier,
            status=Agent.Status.QUEUED
        )
        
        # Stagger spawn ticks
        spawn_tick = world.current_tick + (i // 2) + 1
        
        SpawnQueue.objects.get_or_create(
            agent=agent,
            world=world,
            defaults={'spawn_tick': spawn_tick}
        )
        print(f"Agent {agent.id} ({persona}) queued for tick {spawn_tick}")

if __name__ == '__main__':
    bulk_spawn(10)
