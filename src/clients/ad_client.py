import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
# Change this to point to your AdService host/port
HOST = os.getenv("AD_SERVICE_HOST", "localhost")
PORT = int(os.getenv("AD_SERVICE_PORT", 9555))


def get_stub():
    """Create and return an AdService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.AdServiceStub(channel)


def get_ads(context_keys):
    """
    Call GetAds RPC on AdService.

    Args:
        context_keys (list[str]): list of strings describing context
    """
    stub = get_stub()
    request = demo_pb2.AdRequest(context_keys=context_keys)
    response = stub.GetAds(request)

    print("📢 Ads received:")
    for ad in response.ads:
        print(f" - {ad.text} (url: {ad.redirect_url})")

    return response


def test():
    context = ["electronics", "camera", "sale"]
    get_ads(context)


if __name__ == "__main__":
    test()
