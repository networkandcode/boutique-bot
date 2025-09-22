import os

from dotenv import load_dotenv
import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

load_dotenv()
# Update with your gRPC server host/port
HOST = os.getenv("HEALTH_CHECK_HOST", "localhost")
PORT = int(os.getenv("HEALTH_CHECK_PORT", 50051))


def get_stub():
    """Create and return a Health stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return health_pb2_grpc.HealthStub(channel)


def health_check(service_name=""):
    """
    Call Health.Check RPC.

    Args:
        service_name (str): name of the service to check, empty for overall health
    """
    stub = get_stub()
    request = health_pb2.HealthCheckRequest(service=service_name)

    try:
        response = stub.Check(request)
        status_str = health_pb2.HealthCheckResponse.ServingStatus.Name(response.status)
        print(f"✅ Health status for '{service_name or 'overall'}': {status_str}")
        return response.status
    except grpc.RpcError as e:
        print(f"❌ Health check failed: {e.details()}")
        return None


def test():
    # Check overall health
    health_check()

    # Example: check a specific service
    health_check("CartService")


if __name__ == "__main__":
    test()
