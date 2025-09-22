# example usage: ./test_one_svc ad

#!/bin/bash

# Ensure project root is in PYTHONPATH
export PYTHONPATH=$(pwd)

echo "Running test for $1"
uv run "clients/${1}_client.py"
echo "---------------------------------"
