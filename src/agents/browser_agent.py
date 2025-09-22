from .agent_class import AgentClass

browser_agent = AgentClass(
    name="🌐 Browser",
    instruction="""You are an agent who can open the browser, 
        access the pages, 
        perform tasks on them and retrieve information.
    """,
    server_names=["playwright"],
)
