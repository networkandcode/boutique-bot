import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
HOST = os.getenv("RECOMMENDATION_SERVICE_HOST", "localhost")
PORT = int(
    os.getenv("RECOMMENDATION_SERVICE_PORT", 8080)
)  # adjust to RecommendationService port


def get_stub():
    """Create and return a RecommendationService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.RecommendationServiceStub(channel)


def list_recommendations(user_id: str, product_ids: list[str]):
    """Call ListRecommendations RPC."""
    stub = get_stub()
    request = demo_pb2.ListRecommendationsRequest(
        user_id=user_id, product_ids=product_ids
    )
    response = stub.ListRecommendations(request)

    print(f"✨ Recommendations for user {user_id}:")
    for pid in response.product_ids:
        print(f"- {pid}")
    return response


def test():
    user_id = "user-123"
    product_ids = ["product-abc", "product-xyz"]

    list_recommendations(user_id, product_ids)


if __name__ == "__main__":
    test()
