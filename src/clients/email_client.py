import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
# Update this to match your deployment
HOST = os.getenv("EMAIL_SERVICE_HOST", "localhost")
PORT = int(os.getenv("EMAIL_SERVICE_PORT", 5000))


def get_stub():
    """Create and return an EmailService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.EmailServiceStub(channel)


def send_order_confirmation(email: str, order: dict):
    """
    Call SendOrderConfirmation RPC on EmailService.

    Args:
        email (str): Customer's email address
        order (dict): Dictionary with keys:
                      - order_id
                      - shipping_tracking_id
                      - shipping_address (dict with street_address, city, state, country, zip_code)
                      - shipping_cost (dict with currency_code, units, nanos)
                      - items (list of dicts with {product_id, quantity, cost})
    """
    stub = get_stub()

    # Build order items
    order_items = []
    for item in order["items"]:
        order_items.append(
            demo_pb2.OrderItem(
                item=demo_pb2.CartItem(
                    product_id=item["product_id"], quantity=item["quantity"]
                ),
                cost=demo_pb2.Money(
                    currency_code=item["cost"]["currency_code"],
                    units=item["cost"]["units"],
                    nanos=item["cost"].get("nanos", 0),
                ),
            )
        )

    # Build request
    request = demo_pb2.SendOrderConfirmationRequest(
        email=email,
        order=demo_pb2.OrderResult(
            order_id=order["order_id"],
            shipping_tracking_id=order["shipping_tracking_id"],
            shipping_address=demo_pb2.Address(
                street_address=order["shipping_address"]["street_address"],
                city=order["shipping_address"]["city"],
                state=order["shipping_address"]["state"],
                country=order["shipping_address"]["country"],
                zip_code=order["shipping_address"]["zip_code"],
            ),
            shipping_cost=demo_pb2.Money(
                currency_code=order["shipping_cost"]["currency_code"],
                units=order["shipping_cost"]["units"],
                nanos=order["shipping_cost"].get("nanos", 0),
            ),
            items=order_items,
        ),
    )

    # Call service
    stub.SendOrderConfirmation(request)
    print(f"📧 Order confirmation sent to {email}")


def test():
    email = "customer@example.com"
    order = {
        "order_id": "order-456",
        "shipping_tracking_id": "track-9999",
        "shipping_address": {
            "street_address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "zip_code": 10001,
        },
        "shipping_cost": {"currency_code": "USD", "units": 5, "nanos": 0},
        "items": [
            {
                "product_id": "product-abc",
                "quantity": 2,
                "cost": {"currency_code": "USD", "units": 10, "nanos": 0},
            },
            {
                "product_id": "product-xyz",
                "quantity": 1,
                "cost": {"currency_code": "USD", "units": 20, "nanos": 0},
            },
        ],
    }

    send_order_confirmation(email, order)


if __name__ == "__main__":
    test()
