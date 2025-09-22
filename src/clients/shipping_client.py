import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
HOST = os.getenv("SHIPPING_SERVICE_HOST", "localhost")
PORT = int(
    os.getenv("SHIPPING_SERVICE_PORT", 50051)
)  # adjust to your ShippingService port


def get_stub():
    """Create and return a ShippingService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.ShippingServiceStub(channel)


def get_quote(address: dict, items: list):
    """Call GetQuote RPC."""
    stub = get_stub()
    request = demo_pb2.GetQuoteRequest(
        address=demo_pb2.Address(
            street_address=address["street_address"],
            city=address["city"],
            state=address["state"],
            country=address["country"],
            zip_code=address["zip_code"],
        ),
        items=[
            demo_pb2.CartItem(product_id=i["product_id"], quantity=i["quantity"])
            for i in items
        ],
    )
    response = stub.GetQuote(request)

    print(
        f"📦 Shipping quote: {response.cost_usd.units}.{str(response.cost_usd.nanos).zfill(2)} {response.cost_usd.currency_code}"
    )
    return response


def ship_order(address: dict, items: list):
    """Call ShipOrder RPC."""
    stub = get_stub()
    request = demo_pb2.ShipOrderRequest(
        address=demo_pb2.Address(
            street_address=address["street_address"],
            city=address["city"],
            state=address["state"],
            country=address["country"],
            zip_code=address["zip_code"],
        ),
        items=[
            demo_pb2.CartItem(product_id=i["product_id"], quantity=i["quantity"])
            for i in items
        ],
    )
    response = stub.ShipOrder(request)

    print(f"✅ Order shipped! Tracking ID: {response.tracking_id}")
    return response


def test():
    # Example address + items
    address = {
        "street_address": "123 Hackathon St",
        "city": "Bangalore",
        "state": "KA",
        "country": "India",
        "zip_code": 560001,
    }
    items = [
        {"product_id": "product-abc", "quantity": 2},
        {"product_id": "product-xyz", "quantity": 1},
    ]

    # First get a quote
    get_quote(address, items)

    # Then ship the order
    ship_order(address, items)


if __name__ == "__main__":
    test()
