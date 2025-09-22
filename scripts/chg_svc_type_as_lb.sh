kubectl patch svc $1 -n default -p '{"spec": {"type": "LoadBalancer"}}'
