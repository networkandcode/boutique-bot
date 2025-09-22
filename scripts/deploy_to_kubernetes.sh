kubectl create cm mcp-agent-config --from-file=mcp_agent.config.yaml
kubectl create cm boutique-bot-env --from-env-file=.env.kubernetes
kubectl create secret generic mcp-agent-secrets --from-file=mcp_agent.secrets.yaml
kubectl apply -f kubernetes-manifests/