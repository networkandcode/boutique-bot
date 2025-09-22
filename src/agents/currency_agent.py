from .agent_class import AgentClass

from clients.currency_client import get_supported_currencies, convert
from clients.health_check_client import health_check

currency_agent = AgentClass(
    name="💵 Currency",
    instruction="""You are an agent who can access the currency service API,
        get supported currencies and convert amounts via gRPC.
    """,
    functions=[health_check, get_supported_currencies, convert],
)
