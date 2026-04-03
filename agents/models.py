from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from worlds.models import World

class Agent(models.Model):
    class Status(models.TextChoices):
        QUEUED = 'QUEUED', _('Queued')
        ACTIVE = 'ACTIVE', _('Active')
        DEAD = 'DEAD', _('Dead')
        BANKRUPT = 'BANKRUPT', _('Bankrupt')

    class Persona(models.TextChoices):
        AGGRESSIVE_RAIDER = 'AGGRESSIVE_RAIDER', _('Aggressive Raider')
        ECONOMIC_TRADER = 'ECONOMIC_TRADER', _('Economic Trader')
        DIPLOMAT = 'DIPLOMAT', _('Diplomat')
        EXPLORER = 'EXPLORER', _('Explorer')
        OPPORTUNIST = 'OPPORTUNIST', _('Opportunist')

    class IntelligenceTier(models.TextChoices):
        TIER_1 = 'TIER_1', _('Tier 1 (Basic)')
        TIER_2 = 'TIER_2', _('Tier 2 (Advanced)')
        TIER_3 = 'TIER_3', _('Tier 3 (Elite)')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agents')
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='agents', null=True, blank=True)
    
    # Configuration
    persona = models.CharField(max_length=50, choices=Persona.choices)
    intelligence_tier = models.CharField(
        max_length=20, 
        choices=IntelligenceTier.choices,
        default=IntelligenceTier.TIER_1
    )
    
    # Attributes
    energy = models.FloatField(default=100.0)
    hunger = models.FloatField(default=0.0)
    wealth = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    reputation = models.IntegerField(default=0)
    
    # Position
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    
    # Blockchain / Economy
    wallet_address = models.CharField(max_length=255, null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.QUEUED
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    spawned_at = models.DateTimeField(null=True, blank=True)
    died_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Agent {self.id} ({self.persona}) - {self.owner.username}"

class SpawnQueue(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, related_name='queue_entry')
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='spawn_queue')
    
    spawn_tick = models.PositiveIntegerField(help_text="The tick at which the agent should spawn")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['spawn_tick', 'created_at']

    def __str__(self):
        return f"Queue: {self.agent} for World {self.world.season_number} at tick {self.spawn_tick}"
