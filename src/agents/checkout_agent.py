from .agent_class import AgentClass

from clients.checkout_client import place_order
from clients.health_check_client import health_check

checkout_agent = AgentClass(
    name="💳 Checkout",
    instruction="""You are an agent who can access the checkout service API,
        place orders via gRPC, and interact with other microservices if needed.
    """,
    functions=[health_check, place_order],
)
