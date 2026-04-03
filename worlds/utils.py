from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def schedule_world_tick(world):
    """
    Creates or updates the periodic task for the world's tick.
    """
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=world.tick_interval,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.update_or_create(
        name=f'World {world.id} Tick',
        defaults={
            'interval': schedule,
            'task': 'worlds.tasks.process_world_tick',
            'args': json.dumps([world.id]),
            'enabled': True,
        }
    )

def stop_world_tick(world):
    """
    Disables the periodic task for the world's tick.
    """
    PeriodicTask.objects.filter(name=f'World {world.id} Tick').update(enabled=False)
