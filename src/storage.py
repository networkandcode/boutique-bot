# storage.py
import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

REDIS_HOST = os.getenv("REDIS_CHAT_HISTORY_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_CHAT_HISTORY_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_CHAT_HISTORY_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_CHAT_HISTORY_PASSWORD", None)

# Redis keys
CHATS_KEY = "chat_app:chats"
SELECTED_AGENT_KEY = "chat_app:selected_agent"
CURRENT_CHAT_KEY = "chat_app:current_chat"

# Connect to Redis
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,  # automatically decode strings
)


def save_chats(chats, selected_agent=None, current_chat=None):
    """
    Save chat sessions and current selection to Redis.
    """
    r.set(CHATS_KEY, json.dumps(chats))
    if selected_agent:
        r.set(SELECTED_AGENT_KEY, selected_agent)
    if current_chat:
        r.set(CURRENT_CHAT_KEY, current_chat)


def load_chats():
    """
    Load chat sessions and last selected agent/chat from Redis.
    Returns (chats dict, selected_agent_name, current_chat_id)
    """
    chats_json = r.get(CHATS_KEY)
    chats = json.loads(chats_json) if chats_json else {}

    selected_agent = r.get(SELECTED_AGENT_KEY)
    current_chat = r.get(CURRENT_CHAT_KEY)

    return chats, selected_agent, current_chat


def generate_chat_name(messages, max_words: int = 20):
    """
    Generate a chat name based on the last user message.
    """
    if not messages:
        return ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            words = msg["content"].split()
            preview = " ".join(words[:max_words])
            return preview + ("..." if len(words) > max_words else "")
    return ""
