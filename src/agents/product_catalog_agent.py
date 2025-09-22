from .agent_class import AgentClass

from clients.product_catalog_client import list_products, get_product, search_products
from clients.health_check_client import health_check

product_catalog_agent = AgentClass(
    name="🛍️ ProductCatalog",
    instruction="""You are an agent who can access the product catalog service API,
        list products, get product details, and search products via gRPC.
    """,
    functions=[health_check, list_products, get_product, search_products],
)
