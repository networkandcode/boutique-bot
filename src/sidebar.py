import uuid
import streamlit as st
import agents


def render_sidebar(save_chats_func):
    st.sidebar.title("Options")

    # Agent dictionary
    agents_dict = {getattr(agents, a).name: getattr(agents, a) for a in agents.__all__}
    agent_names = list(agents_dict.keys())

    # Ensure session defaults exist
    default_agent = st.session_state.get(
        "selected_agent_name", agent_names[0] if agent_names else None
    )
    idx = agent_names.index(default_agent) if default_agent in agent_names else 0

    # Agent selection
    selected_agent_name = st.sidebar.selectbox(
        "Choose an agent:",
        agent_names,
        index=idx,
    )
    st.session_state["selected_agent_name"] = selected_agent_name
    st.sidebar.write("")

    # Ensure agent entry exists in session_state
    if selected_agent_name not in st.session_state.get("chats", {}):
        st.session_state.setdefault("chats", {})[selected_agent_name] = {}

    agent_chats = st.session_state["chats"][selected_agent_name]
    selected_chat_id = st.session_state.get("current_chat_id")

    # Start new chat
    if st.sidebar.button("➕ Start new chat"):
        new_chat_id = str(uuid.uuid4())
        st.session_state["chats"][selected_agent_name][new_chat_id] = []
        st.session_state["current_chat_id"] = new_chat_id
        save_chats_func(
            st.session_state["chats"], selected_agent_name, new_chat_id
        )
        selected_chat_id = new_chat_id

    # Chat selector dropdown
    existing_chat_ids = list(agent_chats.keys())
    if existing_chat_ids:

        def format_chat_name(cid: str) -> str:
            msgs = agent_chats[cid]
            if not msgs:
                return f"Chat {cid[:8]}"
            for msg in reversed(msgs):
                if msg["role"] == "user":
                    text = msg["content"].replace("\n", " ").strip()
                    preview = text[:20] + ("…" if len(text) > 20 else "")
                    return preview
            return f"Chat {cid[:8]}"

        selected_chat_id = st.sidebar.selectbox(
            "Choose a chat session:",
            existing_chat_ids,
            format_func=format_chat_name,
            index=(
                existing_chat_ids.index(selected_chat_id)
                if selected_chat_id in existing_chat_ids
                else 0
            ),
        )
        st.session_state["current_chat_id"] = selected_chat_id

        # Delete button at the bottom
        if st.sidebar.button("🗑️ Delete Current Chat"):
            st.session_state["chats"][selected_agent_name].pop(selected_chat_id, None)
            remaining = list(st.session_state["chats"][selected_agent_name].keys())
            st.session_state["current_chat_id"] = remaining[0] if remaining else None
            save_chats_func(
                st.session_state["chats"],
                selected_agent_name,
                st.session_state["current_chat_id"],
            )
            st.rerun()

    return selected_agent_name, selected_chat_id
