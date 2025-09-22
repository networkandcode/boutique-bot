mkdir -p generated
uv run python -m grpc_tools.protoc -I$HOME/microservices-demo/protos/ --python_out=./generated --grpc_python_out=./generated demo.proto
uv run python -m grpc_tools.protoc -I../protos/grpc/health/v1 --python_out=./generated --grpc_python_out=./generated health.proto