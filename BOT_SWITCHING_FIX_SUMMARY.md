# Bot Session Management Fix

## Problem
When users were chatting with a bot (e.g., quotation bot) and sent a number (e.g., "2") as part of their conversation, the system was incorrectly interpreting that number as a request to switch bots rather than a message to the current bot.

For example:
- User chatting with quotation bot sends "2" as a product quantity
- System switched them to the dc bot instead of sending "2" to the quotation bot

## Solution
Modified the bot session management logic in `main.py` to:

1. **Remove automatic bot switching**: Numbers sent during a bot session are no longer automatically interpreted as bot switch commands.

2. **Introduce explicit switch command**: Added a new `/switch [number]` command that users must use to switch bots:
   - `/switch 1` - Switch to grn bot
   - `/switch 2` - Switch to dc bot
   - `/switch 3` - Switch to expense bot
   - `/switch 4` - Switch to quotation bot

3. **Preserve existing functionality**:
   - Initial bot selection by sending a number still works
   - `/bots` command still works
   - All other functionality remains unchanged

## Files Modified
- `main.py` - Updated the bot switching logic
- `test_functionality.py` - Updated tests to reflect new switch command
- `test_comprehensive_fix.py` - Created comprehensive test for the fix
- `USAGE_GUIDE.md` - Updated documentation for new behavior

## Testing
Verified the fix with comprehensive tests that confirm:
1. Numbers sent during bot sessions are forwarded to the bot as messages
2. `/switch [number]` properly switches bots
3. Initial bot selection still works
4. All other functionality remains intact

## Impact
This change resolves the user confusion where legitimate numeric input was being misinterpreted as bot switching commands, making the bot interface more intuitive and preventing accidental bot switches.