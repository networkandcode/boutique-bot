from .agent_class import AgentClass

from clients.payment_client import charge
from clients.health_check_client import health_check

payment_agent = AgentClass(
    name="💰 Payment",
    instruction="""You are an agent who can access the payment service API,
        process payments via gRPC.
    """,
    functions=[health_check, charge],
)
