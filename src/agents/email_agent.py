from .agent_class import AgentClass

from clients.email_client import send_order_confirmation
from clients.health_check_client import health_check

email_agent = AgentClass(
    name="📧 Email",
    instruction="""You are an agent who can access the email service API,
        send order confirmation emails via gRPC.
    """,
    functions=[health_check, send_order_confirmation],
)
