from django.db import models
from agents.models import Agent
from worlds.models import World

class WorldEvent(models.Model):
    class Severity(models.TextChoices):
        INFO = 'INFO', 'Info'
        WARNING = 'WARNING', 'Warning'
        CRITICAL = 'CRITICAL', 'Critical'
        DRAMA = 'DRAMA', 'Drama'

    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='events')
    tick = models.PositiveIntegerField()
    
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    
    event_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.INFO)
    
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tick', '-created_at']

    def __str__(self):
        return f"W{self.world.season_number} T{self.tick}: {self.event_type}"
