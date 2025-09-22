import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
HOST = os.getenv("PRODUCT_CATALOG_SERVICE_HOST", "localhost")
PORT = int(
    os.getenv("PRODUCT_CATALOG_SERVICE_PORT", 3550)
)  # adjust to ProductCatalogService port


def get_stub():
    """Create and return a ProductCatalogService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.ProductCatalogServiceStub(channel)


def list_products():
    """Call ListProducts RPC."""
    stub = get_stub()
    request = demo_pb2.Empty()
    response = stub.ListProducts(request)

    print("📦 Available Products:")
    for p in response.products:
        print(
            f"- {p.id}: {p.name} | {p.price_usd.units}.{str(p.price_usd.nanos).zfill(2)} {p.price_usd.currency_code}"
        )
    return response


def get_product(product_id: str):
    """Call GetProduct RPC."""
    stub = get_stub()
    request = demo_pb2.GetProductRequest(id=product_id)
    response = stub.GetProduct(request)

    print(f"🔎 Product {product_id}: {response.name} ({response.description})")
    return response


def search_products(query: str):
    """Call SearchProducts RPC."""
    stub = get_stub()
    request = demo_pb2.SearchProductsRequest(query=query)
    response = stub.SearchProducts(request)

    print(f"🔍 Search results for '{query}':")
    for p in response.results:
        print(
            f"- {p.id}: {p.name} | {p.price_usd.units}.{str(p.price_usd.nanos).zfill(2)} {p.price_usd.currency_code}"
        )
    return response


def test():
    # List all products
    list_products()

    # Search for a product
    search_products("shirt")

    # Get one specific product
    get_product("product-abc")  # replace with a valid ID from your catalog


if __name__ == "__main__":
    test()
