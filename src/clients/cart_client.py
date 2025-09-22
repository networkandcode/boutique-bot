import os

from dotenv import load_dotenv
import grpc

from generated import demo_pb2, demo_pb2_grpc

load_dotenv()
HOST = os.getenv("CART_SERVICE_HOST", "localhost")
PORT = os.getenv("CART_SERVICE_PORT", 7070)


def get_stub():
    """Create and return a CartService stub."""
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    return demo_pb2_grpc.CartServiceStub(channel)


def add_item(user_id: str, product_id: str, quantity: int):
    """Call AddItem RPC."""
    stub = get_stub()
    request = demo_pb2.AddItemRequest(
        user_id=user_id,
        item=demo_pb2.CartItem(product_id=product_id, quantity=quantity),
    )
    stub.AddItem(request)
    print(f"✅ Added {quantity} x {product_id} for user {user_id}")


def get_cart(user_id: str):
    """Call GetCart RPC and return cart contents."""
    stub = get_stub()
    request = demo_pb2.GetCartRequest(user_id=user_id)
    cart = stub.GetCart(request)

    print(f"🛒 Cart for {user_id}:")
    if not cart.items:
        print("  (empty)")
    for item in cart.items:
        print(f"  - {item.product_id} x {item.quantity}")
    return cart


def empty_cart(user_id: str):
    """Call EmptyCart RPC."""
    stub = get_stub()
    request = demo_pb2.EmptyCartRequest(user_id=user_id)
    stub.EmptyCart(request)
    print(f"🗑️ Emptied cart for {user_id}")


def test():
    user_id = "user-123"

    # Add items
    add_item(user_id, "product-abc", 2)
    add_item(user_id, "product-xyz", 1)

    # View cart
    get_cart(user_id)

    # Empty cart
    empty_cart(user_id)

    # Verify empty
    get_cart(user_id)


if __name__ == "__main__":
    test()
