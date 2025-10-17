# Product Selection Fix

## Problem
When users were chatting with the quotation bot and reached the product selection phase where they needed to select a product by sending a number (e.g., "1" for the first product), the system was incorrectly interpreting that number as a bot switch command. This caused users to be switched to the grn bot (bot #1) instead of selecting the product they wanted.

## Solution
Modified the bot switching logic to differentiate between:
1. Numbers sent as part of a conversation with a bot (e.g., product selection)
2. Numbers sent as bot switch commands

### Key Changes
1. **Removed automatic bot switching during sessions**: Numbers sent during a bot session are no longer automatically interpreted as bot switch commands.
2. **Bot switching only occurs after explicit bot list request**: Users must first send "/bots", "bots", or "list" to see the bot selection menu, then send a number to switch bots.
3. **Maintained session-based architecture**: All changes work within the existing session-based framework.

## Behavior
- When a user is in a session with a bot (e.g., quotation bot) and sends a number (e.g., "1"), it is forwarded to the bot as part of the conversation
- When a user sends "/bots", "bots", or "list", their session is cleared and they see the bot selection menu
- Only after seeing the bot selection menu can users send a number to switch bots

## Testing
Verified the fix with comprehensive tests that confirm:
1. Product selection numbers are correctly forwarded to the quotation bot
2. Users remain in the quotation bot during product selection
3. Bot switching only occurs after explicitly requesting the bot list
4. Session management works correctly throughout the process

## Benefits
- Users can now properly select products in the quotation bot without being switched to another bot
- The conversation flow is more intuitive and matches user expectations
- Bot switching is still possible but requires explicit action from the user