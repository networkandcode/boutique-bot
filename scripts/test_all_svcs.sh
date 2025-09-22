#!/bin/bash

# Ensure project root is in PYTHONPATH
export PYTHONPATH=$(pwd)

# List of all client test scripts
clients=(
    "clients/cart_client.py"
    "clients/ad_client.py"
    "clients/checkout_client.py"
    "clients/email_client.py"
    "clients/payment_client.py"
    "clients/recommendation_client.py"
    "clients/currency_client.py"
    "clients/health_check_client.py"
    "clients/product_catalog_client.py"
    "clients/shipping_client.py"
)

# Run each client test with uv
for client in "${clients[@]}"; do
    echo "Running tests for $client"
    uv run "$client"
    echo "---------------------------------"
done
