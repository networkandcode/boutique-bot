from .agent_class import AgentClass

from clients.health_check_client import health_check

health_check_agent = AgentClass(
    name="❤️‍🩹 HealthCheck",
    instruction="""You are an agent who can check the health status of any gRPC service
        in the system using the standard gRPC Health API.
    """,
    functions=[health_check],
)
