import logging
from celery import shared_task
from django.db import transaction
from agents.models import Agent
from worlds.models import World
from events.models import WorldEvent

logger = logging.getLogger(__name__)

@shared_task
def execute_agent_cognition(agent_id, tick):
    """
    Handles agent reasoning and action execution.
    """
    try:
        agent = Agent.objects.get(id=agent_id, status=Agent.Status.ACTIVE)
        world = agent.world
        
        # 1. Gather Context (World State Snapshot around agent)
        context = gather_agent_context(agent, world)
        
        # 2. Plan Action (This is where the LLM or Sandbox would live)
        # For now, let's use a simple placeholder or call a reasoning service
        action = plan_agent_action(agent, context)
        
        # 3. Execute Action
        execute_action(agent, action, tick)
        
        # 4. Energy/Hunger Decay
        apply_survival_decay(agent)
        
    except Agent.DoesNotExist:
        logger.warning(f"Agent {agent_id} not found or not active.")
    except Exception as e:
        logger.exception(f"Error in agent cognition for {agent_id}: {e}")

def gather_agent_context(agent, world):
    """
    Returns a representation of what the agent 'sees'.
    """
    # Placeholder: List nearby resources, agents, etc.
    return {
        "position": {"x": agent.position_x, "y": agent.position_y},
        "stats": {"energy": agent.energy, "wealth": float(agent.wealth)},
        "nearby_resources": list(world.resource_nodes.all()[:5].values()),
        "tick": world.current_tick
    }

def plan_agent_action(agent, context):
    """
    Decide what to do based on context and persona using Gemini.
    """
    from core.cognition.gemini_client import GeminiClient
    from core.cognition.prompts import get_system_instruction, get_action_prompt
    import json

    client = GeminiClient()
    system_instruction = get_system_instruction(agent)
    prompt = get_action_prompt(context)
    
    response_text = client.generate_response(prompt, system_instruction=system_instruction)
    
    if response_text:
        try:
            # Simple cleaning for common markdown noise
            cleaned_text = response_text.replace('```json', '').replace('```', '').strip()
            action = json.loads(cleaned_text)
            return action
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse Gemini response for agent {agent.id}: {e}")
            logger.debug(f"Raw response: {response_text}")
    
    # Fallback if planning fails
    return {"action": "move", "direction": "random"}

def execute_action(agent, action, tick):
    """
    Validates and applies the action to the world state.
    """
    with transaction.atomic():
        agent = Agent.objects.select_for_update().get(id=agent.id)
        
        action_type = action.get("action", "").lower()
        target = action.get("target")
        reasoning = action.get("reasoning", "")
        
        description = f"Action: {action_type}. Reasoning: {reasoning}"
        
        if action_type == "move":
            import random
            # Move towards a target or random direction
            agent.position_x += random.randint(-1, 1)
            agent.position_y += random.randint(-1, 1)
            description = f"Moved to ({agent.position_x}, {agent.position_y}): {reasoning}"
        
        elif action_type == "gather":
            # Logic to find resource at position
            resource = agent.world.resource_nodes.filter(
                position_x=agent.position_x, 
                position_y=agent.position_y,
                quantity__gt=0
            ).first()
            
            if resource:
                resource.quantity -= 1
                resource.save()
                agent.energy += 5
                description = f"Gathered {resource.resource_type}. Energy increased."
            else:
                description = "Tried to gather but no resources found at this position."
        
        elif action_type == "attack":
            # Placeholder for combat
            description = f"Attempted to attack {target}. (Combat engine pending)"
            
        elif action_type == "trade":
            # Placeholder for trading
            description = f"Proposed trade to {target}. (Marketplace engine pending)"
            
        agent.save()
        
        # Log drama
        WorldEvent.objects.create(
            world=agent.world,
            tick=tick,
            agent=agent,
            event_type="AGENT_ACTION",
            description=description,
            severity=WorldEvent.Severity.DRAMA if action_type == "attack" else WorldEvent.Severity.INFO,
            metadata={"action": action}
        )

def apply_survival_decay(agent):
    """
    Reduces energy and increases hunger every tick.
    """
    agent.energy -= 1.0 # Basic decay
    if agent.energy <= 0:
        agent.status = Agent.Status.DEAD
        agent.energy = 0
        
        WorldEvent.objects.create(
            world=agent.world,
            tick=agent.world.current_tick,
            agent=agent,
            event_type="AGENT_DIED",
            description="Agent died of exhaustion."
        )
    agent.save()
