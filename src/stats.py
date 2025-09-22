import asyncio
import streamlit as st
import pandas as pd
import plotly.express as px
import agents

from storage import load_chats

# Prepare agent list
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
                except Exception:
                    agent.tool_list = []
            tool_map[agent.name] = agent.tool_list
        return tool_map

    return asyncio.run(fetch_tools())

def get_agent_stats(chats, tool_map):
    """
    Compute stats per agent:
    - user_requests: total user messages
    - num_chats: total chats per agent
    - num_tools: total tools per agent (cached)
    """
    stats = {}
    for agent_name, chat_dict in chats.items():
        user_requests = sum(
            1
            for messages in chat_dict.values()
            for msg in messages
            if msg.get("role") == "user"
        )
        num_chats = len(chat_dict)
        num_tools = len(tool_map.get(agent_name, []))
        stats[agent_name] = {
            "User Requests": user_requests,
            "Chats": num_chats,
            "Tools": num_tools,
        }
    return stats

def main():
    st.set_page_config(page_title="Agent Stats", layout="wide")
    st.title("Agent Statistics")
    st.caption("Overview of requests, chats, and tools per agent.")

    # Color selection
    color_choice = st.radio(
        "Choose chart color:",
        options=["🧡 Orange", "💙 Blue", "💜 Purple"],
        index=0,
        horizontal=True
    )
    if color_choice.startswith("🧡"):
        color_scale = ["#ff7f50", "#ff4500", "#ff6347", "#ff8c00", "#ffa500"]
    elif color_choice.startswith("💙"):
        color_scale = ["#1f77b4", "#2196f3", "#00bfff", "#87cefa", "#add8e6"]
    else:  # 💜 Purple
        color_scale = ["#9b59b6", "#8e44ad", "#a569bd", "#af7ac5", "#d2b4de"]

    # Load chat history
    chats, _, _ = load_chats()
    if not chats:
        st.info("No chat data available yet.")
        return

    # Load cached tools
    tool_map = load_all_tools()

    # Compute stats
    stats_dict = get_agent_stats(chats, tool_map)

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(stats_dict, orient="index").reset_index()
    df.rename(columns={"index": "Agent"}, inplace=True)
    df.index = df.index + 1  # table index starts from 1

    # Table in expander
    with st.expander("Summary Table", expanded=True):
        st.dataframe(df, width='stretch')

    # Requests chart
    with st.expander("Requests per Agent", expanded=True):
        fig1 = px.bar(
            df,
            x="Agent",
            y="User Requests",
            text="User Requests",
            title="Number of Requests per Agent",
            height=500,
            color="User Requests",
            color_continuous_scale=color_scale
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, width='stretch')

    # Chats chart
    with st.expander("Chats per Agent", expanded=True):
        fig2 = px.bar(
            df,
            x="Agent",
            y="Chats",
            text="Chats",
            title="Number of Chats per Agent",
            height=500,
            color="Chats",
            color_continuous_scale=color_scale
        )
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, width='stretch')

    # Tools chart
    with st.expander("Tools per Agent", expanded=True):
        fig3 = px.bar(
            df,
            x="Agent",
            y="Tools",
            text="Tools",
            title="Number of Tools per Agent",
            height=500,
            color="Tools",
            color_continuous_scale=color_scale
        )
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, width='stretch')

if __name__ == "__main__":
    main()
