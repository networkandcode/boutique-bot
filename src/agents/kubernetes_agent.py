from .agent_class import AgentClass

kubernetes_agent = AgentClass(
    name="☸️ Kubernetes",
    instruction="""You are an agent who can access the kubernetes cluster,
        perform operations on kubernetes objects.
    """,
    server_names=["kubernetes"],
)
