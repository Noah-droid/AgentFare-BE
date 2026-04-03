import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from worlds.models import World
from agents.models import Agent
from economy.models import FuelBalance

def seed():
    # 1. Create superuser if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        print("Superuser 'admin' created.")

    user = User.objects.get(username='admin')
    
    # 2. Assign initial fuel
    FuelBalance.objects.get_or_create(user=user, defaults={'amount': 1000.0})

    # 3. Create a World
    world, created = World.objects.get_or_create(
        season_number=1,
        defaults={
            'status': World.Status.CREATION,
            'tick_interval': 10, # 10 seconds for testing
            'max_agents': 10
        }
    )
    if created:
        print(f"World Season {world.season_number} created.")

    # 4. Create an Agent for the user
    agent, created = Agent.objects.get_or_create(
        owner=user,
        persona=Agent.Persona.ECONOMIC_TRADER,
        defaults={
            'intelligence_tier': Agent.IntelligenceTier.TIER_2,
            'status': Agent.Status.QUEUED
        }
    )
    if created:
        print(f"Agent {agent.id} created for admin.")

if __name__ == '__main__':
    seed()
