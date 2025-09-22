from .agent_class import AgentClass

from clients.cart_client import add_item, get_cart, empty_cart
from clients.health_check_client import health_check

cart_agent = AgentClass(
    name="🛒 Cart",
    instruction="""You are an agent who can access the cart service api,
        perform operations via grpc.
    """,
    functions=[
        health_check,
        add_item,
        get_cart,
        empty_cart,
    ],
)
