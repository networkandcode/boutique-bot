from .agent_class import AgentClass

from clients.ad_client import get_ads
from clients.health_check_client import health_check

ad_agent = AgentClass(
    name="📢 Ad",
    instruction="""You are an agent who can access the ad service API,
        fetch advertisements via gRPC based on context keys.
    """,
    functions=[health_check, get_ads],
)
