import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
# Update host/port for your PaymentService
HOST = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
PORT = int(os.getenv("PAYMENT_SERVICE_PORT", 50051))


def get_stub():
    """Create and return a PaymentService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.PaymentServiceStub(channel)


def charge(amount: dict, card: dict):
    """
    Call Charge RPC on PaymentService.

    Args:
        amount (dict): {currency_code, units, nanos}
        card (dict): {credit_card_number, credit_card_cvv, credit_card_expiration_year, credit_card_expiration_month}
    """
    stub = get_stub()

    request = demo_pb2.ChargeRequest(
        amount=demo_pb2.Money(
            currency_code=amount["currency_code"],
            units=amount["units"],
            nanos=amount.get("nanos", 0),
        ),
        credit_card=demo_pb2.CreditCardInfo(
            credit_card_number=card["credit_card_number"],
            credit_card_cvv=card["credit_card_cvv"],
            credit_card_expiration_year=card["credit_card_expiration_year"],
            credit_card_expiration_month=card["credit_card_expiration_month"],
        ),
    )

    response = stub.Charge(request)

    if response.error:
        print(f"❌ Payment failed: {response.error}")
    else:
        print(f"✅ Payment success, transaction ID: {response.transaction_id}")

    return response


def test():
    amount = {"currency_code": "USD", "units": 50, "nanos": 0}
    card = {
        "credit_card_number": "4111111111111111",
        "credit_card_cvv": 123,
        "credit_card_expiration_year": 2028,
        "credit_card_expiration_month": 12,
    }

    charge(amount, card)


if __name__ == "__main__":
    test()
