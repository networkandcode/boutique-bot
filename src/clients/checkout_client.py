import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
# Change these to match your deployment
HOST = os.getenv("CHECKOUT_SERVICE_HOST", "localhost")
PORT = int(os.getenv("CHECKOUT_SERVICE_PORT", 5050))


def get_stub():
    """Create and return a CheckoutService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.CheckoutServiceStub(channel)


def place_order(user_id, user_currency, address, email, credit_card):
    """
    Call PlaceOrder RPC on CheckoutService.

    Args:
        user_id (str): ID of the user
        user_currency (str): Currency code, e.g. "USD"
        address (dict): Dict with keys street_address, city, state, country, zip_code
        email (str): User email
        credit_card (dict): Dict with keys credit_card_number, credit_card_cvv,
                            credit_card_expiration_year, credit_card_expiration_month
    """
    stub = get_stub()

    # Build the request
    request = demo_pb2.PlaceOrderRequest(
        user_id=user_id,
        user_currency=user_currency,
        address=demo_pb2.Address(
            street_address=address["street_address"],
            city=address["city"],
            state=address["state"],
            country=address["country"],
            zip_code=address["zip_code"],
        ),
        email=email,
        credit_card=demo_pb2.CreditCardInfo(
            credit_card_number=credit_card["credit_card_number"],
            credit_card_cvv=credit_card["credit_card_cvv"],
            credit_card_expiration_year=credit_card["credit_card_expiration_year"],
            credit_card_expiration_month=credit_card["credit_card_expiration_month"],
        ),
    )

    # Call service
    response = stub.PlaceOrder(request)

    print(f"✅ Order placed successfully. Order ID: {response.order.order_id}")
    print(f"   Tracking ID: {response.order.shipping_tracking_id}")
    print(
        f"   Shipping to: {response.order.shipping_address.street_address}, {response.order.shipping_address.city}"
    )
    return response


def test():
    user_id = "user-123"
    user_currency = "USD"
    email = "test@example.com"

    address = {
        "street_address": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
        "zip_code": 94105,
    }

    credit_card = {
        "credit_card_number": "4111111111111111",
        "credit_card_cvv": 123,
        "credit_card_expiration_year": 2026,
        "credit_card_expiration_month": 12,
    }

    place_order(user_id, user_currency, address, email, credit_card)


if __name__ == "__main__":
    test()
