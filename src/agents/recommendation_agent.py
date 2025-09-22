from .agent_class import AgentClass

from clients.recommendation_client import list_recommendations
from clients.health_check_client import health_check

recommendation_agent = AgentClass(
    name="👍 Recommendation",
    instruction="""You are an agent who can access the recommendation service API,
        fetch product recommendations via gRPC based on user ID and context.
    """,
    functions=[health_check, list_recommendations],
)
