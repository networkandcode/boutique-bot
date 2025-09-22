import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
# Update host/port to where your CurrencyService is running
HOST = os.getenv("CURRENCY_SERVICE_HOST", "localhost")
PORT = int(os.getenv("CURRENCY_SERVICE_PORT", 7000))


def get_stub():
    """Create and return a CurrencyService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.CurrencyServiceStub(channel)


def get_supported_currencies():
    """Call GetSupportedCurrencies RPC."""
    stub = get_stub()
    request = demo_pb2.Empty()
    response = stub.GetSupportedCurrencies(request)

    print("🌍 Supported currencies:")
    for code in response.currency_codes:
        print(f" - {code}")
    return response.currency_codes


def convert(from_amount: dict, to_code: str):
    """
    Call Convert RPC.

    Args:
        from_amount (dict): {currency_code, units, nanos}
        to_code (str): target currency code
    """
    stub = get_stub()
    request = demo_pb2.CurrencyConversionRequest(
        from_=demo_pb2.Money(
            currency_code=from_amount["currency_code"],
            units=from_amount["units"],
            nanos=from_amount.get("nanos", 0),
        ),
        to_code=to_code,
    )
    response = stub.Convert(request)

    print(
        f"💱 {from_amount['units']} {from_amount['currency_code']} = "
        f"{response.units}.{str(response.nanos).zfill(2)} {response.currency_code}"
    )
    return response


def test():
    # List currencies
    get_supported_currencies()

    # Convert 100 USD to EUR
    from_amount = {"currency_code": "USD", "units": 100, "nanos": 0}
    convert(from_amount, "EUR")


if __name__ == "__main__":
    test()
