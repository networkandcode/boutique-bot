import asyncio
import streamlit as st
import agents

st.set_page_config(page_title="Boutique Bot - Help", layout="wide")
st.title("Agent Help")
st.markdown("View details about all available agents:")

cols_per_row = 3  # Number of agent cards per row
agent_list = [getattr(agents, a) for a in agents.__all__]


@st.cache_resource
def load_all_tools():
    """
    Ensure that each agent fetches and caches its tools only once.
    Returns a dictionary {agent_name: [tools]}.
    """

    async def fetch_tools():
        tool_map = {}
        for agent in agent_list:
            if not getattr(agent, "tool_list", None):
                try:
                    tools = await agent.list_tools()
                    agent.tool_list = tools.tools  # store on agent
                except Exception as e:
                    agent.tool_list = None
            tool_map[agent.name] = agent.tool_list
        return tool_map

    return asyncio.run(fetch_tools())


def main():
    tool_map = load_all_tools()

    for i in range(0, len(agent_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, agent in enumerate(agent_list[i : i + cols_per_row]):
            with cols[j]:
                with st.container(border=True):
                    st.markdown(f"### {agent.name}")
                    if hasattr(agent, "instruction"):
                        st.markdown(f"**Instruction:** {agent.instruction}")

                    # Tools inside an expander
                    tools = tool_map.get(agent.name)
                    with st.expander("View Tools"):
                        if tools is None:
                            st.warning("_Unable to fetch tools for this agent._")
                        elif not tools:
                            st.info("_No tools available for this agent._")
                        else:
                            for tool in tools:
                                st.markdown(f"- **{tool.name}**: {tool.description}")


if __name__ == "__main__":
    main()
