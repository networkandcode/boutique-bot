from mcp_agent.agents.agent import Agent


class AgentClass(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tools = None

    async def get_tools(self):
        if self.tools is None:
            tools = await self.list_tools()
            self.tools = tools.tools
            return self.tools
