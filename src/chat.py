import asyncio
import streamlit as st
from mcp_agent.app import MCPApp
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM

import agents
from sidebar import render_sidebar
from storage import save_chats, load_chats

# --- Streamlit page setup ---
st.set_page_config(page_title="Boutique Bot - Chat", layout="wide")
st.title("🛍️ Boutique Bot")
st.caption("🎨 Online Boutique AI Assistant powered by Gemini, Streamlit & MCP-Agent")

# --- Initialize MCPApp ---
if "app" not in st.session_state:
    st.session_state["app"] = MCPApp(name="online_boutique_app")
app = st.session_state["app"]

# --- Cache agents dictionary ---
if "agents_dict" not in st.session_state:
    st.session_state["agents_dict"] = {
        getattr(agents, a).name: getattr(agents, a) for a in agents.__all__
    }
agents_dict = st.session_state["agents_dict"]

# --- Cache agent tools ---
if "agent_tools" not in st.session_state:
    st.session_state["agent_tools"] = {}

# --- Load chats ---
if "chats" not in st.session_state:
    chats, last_agent, last_chat = load_chats()
    st.session_state["chats"] = chats
    st.session_state["selected_agent_name"] = last_agent or list(agents_dict.keys())[0]
    st.session_state["current_chat_id"] = last_chat

async def main():
    async with app.run() as agent_app:
        logger = agent_app.logger

        # Sidebar
        selected_agent_name, selected_chat_id = render_sidebar(save_chats)

        # Ensure selected agent exists
        if selected_agent_name not in st.session_state["chats"]:
            st.session_state["chats"][selected_agent_name] = {}

        agent_chats = st.session_state["chats"][selected_agent_name]

        # --- Load or cache tools ---
        selected_agent = agents_dict[selected_agent_name]
        if selected_agent_name not in st.session_state["agent_tools"]:
            async with selected_agent:
                tools_result = await selected_agent.list_tools()
                tools = tools_result.tools
                st.session_state["agent_tools"][selected_agent_name] = tools
        else:
            tools = st.session_state["agent_tools"][selected_agent_name]

        if not tools:
            st.info(f"No tools available for {selected_agent_name} agent.")
            logger.info(f"No tools available for {selected_agent_name} agent.")

        # --- Display chat history ---
        messages = agent_chats.get(selected_chat_id, [])
        if not messages or not selected_chat_id:
            st.info(f"Start a new chat with **{selected_agent_name}** to begin.")
        else:
            for message in messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # --- Handle chat input ---
        prompt = st.chat_input("How can I help you")
        if prompt:
            # User message
            with st.chat_message("user"):
                st.markdown(f"**You:** {prompt}")
            messages.append({"role": "user", "content": prompt})

            # Agent response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    async with selected_agent:
                        llm = await selected_agent.attach_llm(GoogleAugmentedLLM)
                        response = await llm.generate_str(
                            message=prompt,
                            request_params=RequestParams(use_history=True),
                        )
                        st.markdown(response)
            messages.append({"role": "assistant", "content": response})

            # Save updated chat
            st.session_state["chats"][selected_agent_name][selected_chat_id] = messages
            save_chats(
                st.session_state["chats"], selected_agent_name, selected_chat_id
            )

        # --- Update session state ---
        st.session_state["selected_agent_name"] = selected_agent_name
        st.session_state["current_chat_id"] = selected_chat_id

# --- Helper to safely run async in Streamlit ---
def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# --- Run the app ---
run_async(main())  # Note: parentheses create coroutine object
