from django.db import models
from django.conf import settings
from agents.models import Agent
from worlds.models import World

class FuelBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fuel_balance')
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.amount} Fuel"

class Transaction(models.Model):
    class Type(models.TextChoices):
        BUY = 'BUY', ('Buy Fuel')
        SPAWN = 'SPAWN', ('Agent Spawn')
        TICK_MAINTENANCE = 'TICK_MAINTENANCE', ('Maintenance Cost')
        ACTION_COST = 'ACTION_COST', ('Action Cost')
        REWARD = 'REWARD', ('Seasonal Reward')
        BURN = 'BURN', ('Token Burn')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    type = models.CharField(max_length=20, choices=Type.choices)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount}"

class RewardPool(models.Model):
    world = models.OneToOneField(World, on_delete=models.CASCADE, related_name='reward_pool')
    total_tokens = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    
    distribution_rules = models.JSONField(default=dict, help_text="Rules for reward distribution at settlement")
    
    def __str__(self):
        return f"Reward Pool: World {self.world.season_number} - {self.total_tokens} Tokens"
