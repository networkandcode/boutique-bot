import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
import streamlit as st

import agents
from sidebar import render_sidebar
from storage import save_chats, load_chats


async def main():
    async with app.run() as agent_app:
        # get all agents from agents directory
        # forms a dictionary with key as agent display name, and value as the agent object/config
        agents_dict = {
            getattr(agents, a).name: getattr(agents, a) for a in agents.__all__
        }

        # Load chats from database
        chats, last_agent, last_chat = load_chats()

        # set session state for chat history
        if "chats" not in st.session_state:
            st.session_state["chats"] = chats

        # set session state for selected agent name
        if "selected_agent_name" not in st.session_state:
            st.session_state["selected_agent_name"] = (
                last_agent or list(agents_dict.keys())[0]
            )

        # set session state for current chat id
        if "current_chat_id" not in st.session_state:
            st.session_state["current_chat_id"] = last_chat

        # Sidebar
        selected_agent_name, selected_chat_id = render_sidebar(save_chats)

        # Ensure agent exists in session_state
        if selected_agent_name not in st.session_state["chats"]:
            st.session_state["chats"][selected_agent_name] = {}

        agent_chats = st.session_state["chats"][selected_agent_name]

        if not agent_chats or not selected_chat_id:
            st.info(f"Start a new chat with **{selected_agent_name}** to begin.")
            return  # stop here until a chat is created via sidebar

        # Update session state
        st.session_state["selected_agent_name"] = selected_agent_name
        st.session_state["current_chat_id"] = selected_chat_id
        messages = agent_chats.get(selected_chat_id, [])

        # Fetch tools
        selected_agent = agents_dict[selected_agent_name]

        logger = agent_app.logger
        async with selected_agent:
            tools = await selected_agent.list_tools()
            tools = tools.tools
            if not tools:
                st.info(f"No tools available for {selected_agent_name} agent.")
                logger.info(f"No tools available for {selected_agent_name} agent.")

            # Display chat history
            for message in messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # get input from user
            prompt = st.chat_input("How can I help you")  # Always show input
            if prompt:
                # User message
                with st.chat_message("user"):
                    st.markdown(f"**You:** {prompt}")
                messages.append({"role": "user", "content": prompt})

                # Agent response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        llm = await selected_agent.attach_llm(GoogleAugmentedLLM)
                        response = await llm.generate_str(
                            message=prompt,
                            request_params=RequestParams(use_history=True),
                        )
                        st.markdown(response)
                messages.append({"role": "assistant", "content": response})

                # Save updated messages
                st.session_state["chats"][selected_agent_name][
                    selected_chat_id
                ] = messages
                save_chats(
                    st.session_state["chats"], selected_agent_name, selected_chat_id
                )


if __name__ == "__main__":
    app = MCPApp(name="online_boutique_app")
    st.set_page_config(page_title="Boutique Bot - Chat", layout="wide")
    st.title("🛍️ Boutique Bot")
    st.caption(
        "🎨 Online Boutique AI Assistant powered by Gemini, Streamlit & MCP-Agent"
    )
    asyncio.run(main())
