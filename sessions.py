# sessions.py

# In-memory session store: session_id -> bot_name
SESSION_BOT_MAPPING = {}

def set_session_bot(session_id: str, bot_name: str):
    SESSION_BOT_MAPPING[session_id] = bot_name

def get_session_bot(session_id: str):
    return SESSION_BOT_MAPPING.get(session_id)

def clear_session_bot(session_id: str):
    if session_id in SESSION_BOT_MAPPING:
        del SESSION_BOT_MAPPING[session_id]
