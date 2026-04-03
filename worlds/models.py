from django.db import models
from django.utils.translation import gettext_lazy as _

class World(models.Model):
    class Status(models.TextChoices):
        CREATION = 'CREATION', _('Creation')
        ENTRY = 'ENTRY', _('Entry Window')
        ACTIVE = 'ACTIVE', _('Active Simulation')
        ENDGAME = 'ENDGAME', _('Endgame Pressure')
        SETTLEMENT = 'SETTLEMENT', _('Settlement')
        ARCHIVED = 'ARCHIVED', _('Archived')

    season_number = models.PositiveIntegerField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATION
    )
    
    # Configuration
    tick_interval = models.PositiveIntegerField(default=60, help_text="In seconds")
    max_agents = models.PositiveIntegerField(default=50)
    
    # Lifecycle
    current_tick = models.PositiveIntegerField(default=0)
    entry_window_close_tick = models.PositiveIntegerField(default=144) # e.g. 24 hours if 10 min ticks
    
    # World Metadata
    map_size_x = models.PositiveIntegerField(default=100)
    map_size_y = models.PositiveIntegerField(default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        from worlds.utils import schedule_world_tick, stop_world_tick
        
        if self.status in [self.Status.ENTRY, self.Status.ACTIVE, self.Status.ENDGAME]:
            schedule_world_tick(self)
            
            if is_new or self.status == self.Status.ENTRY:
                from worlds.tasks import spawn_world_resources
                spawn_world_resources.delay(self.id)
        else:
            stop_world_tick(self)

    def __str__(self):
        return f"Season {self.season_number} - {self.status}"

class ResourceNode(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='resource_nodes')
    
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    
    resource_type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    
    respawn_tick = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.resource_type} at ({self.position_x}, {self.position_y})"
