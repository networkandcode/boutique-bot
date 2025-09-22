from .agent_class import AgentClass

from clients.shipping_client import get_quote, ship_order
from clients.health_check_client import health_check

shipping_agent = AgentClass(
    name="🚚 Shipping",
    instruction="""You are an agent who can access the shipping service API,
        get shipping quotes and create shipments via gRPC.
    """,
    functions=[health_check, get_quote, ship_order],
)
