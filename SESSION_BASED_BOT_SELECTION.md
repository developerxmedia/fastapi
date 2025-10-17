# Session-Based Bot Selection Implementation

## Problem
The original implementation used `user_id` to track which bot a user was chatting with. This meant that:
1. All sessions for the same user shared the same bot selection
2. If a user started a new session, they would continue with the same bot
3. There was no way to have multiple concurrent conversations with different bots

## Solution
Modified the implementation to use `session_id` instead of `user_id` for tracking bot selections:

### Changes Made

1. **Updated sessions.py**:
   - Changed the session store from `user_id -> bot_name` to `session_id -> bot_name`
   - Renamed functions to reflect session-based tracking:
     - `set_user_bot()` → `set_session_bot()`
     - `get_user_bot()` → `get_session_bot()`
     - `clear_user_bot()` → `clear_session_bot()`

2. **Updated main.py**:
   - Modified all session management functions to use `session_id` instead of `user_id`
   - Updated the `/chatbot` endpoint to track bot selections by `session_id`
   - Added a new endpoint `/current_bot_by_session/{session_id}` to check bot selection by session
   - Updated the `/change_bot` and `/logout` endpoints to use `session_id`
   - Maintained backward compatibility for the existing `/current_bot/{user_id}` endpoint

3. **Behavior Changes**:
   - Each session (identified by `session_id`) now maintains its own bot selection
   - When a new session is started with a different `session_id`, it begins with no bot selected
   - Multiple concurrent sessions can have different bots selected
   - Sessions are completely independent of each other

### Testing
Verified the implementation with comprehensive tests that confirm:
1. Sessions with different `session_id` values maintain independent bot selections
2. Messages within the same session are sent to the correct bot
3. New sessions start fresh without any bot pre-selected
4. Session-specific bot tracking works correctly

### Benefits
- Users can now have multiple concurrent conversations with different bots
- Each session starts fresh, providing a clean slate for new conversations
- Better isolation between different user sessions
- More flexible session management for mobile applications