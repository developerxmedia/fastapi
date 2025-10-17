# Bot Switching Behavior Update

## Changes Made

1. **Removed /switch command requirement**: Users can now switch bots by simply sending a number during a session, rather than requiring the `/switch` command.

2. **Automatic session reset on /bots command**: When a user sends "/bots", "bots", or "list", their current session is automatically cleared, and they see the bot selection menu again.

3. **Simplified bot switching**: During a session, sending any valid bot number (1-4) will immediately switch the user to that bot, with a confirmation message.

## Behavior

- When a user is in a session with a bot (e.g., quotation bot) and sends a number (e.g., "2"), they will switch to the corresponding bot (dc bot) without needing a special command.
- When a user sends "/bots", their session is cleared and they start fresh with the bot selection menu.
- All session management is still based on `session_id` as implemented previously.

## Testing

The new behavior was verified with tests that confirm:
1. Initial bot selection works correctly
2. Messages are sent to the correct bot during a session
3. Bot switching by sending numbers works as expected
4. The /bots command resets the session properly
5. New bot selection after /bots command works correctly

## Benefits

- More intuitive user experience - users can switch bots naturally by sending numbers
- Clear session reset when users want to see all available bots
- No need to remember special commands like `/switch`
- Consistent with the original requirements