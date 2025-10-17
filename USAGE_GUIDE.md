# Bot Gateway Usage Guide

## Initial Interaction
When a user first sends a message (like "hello"), they will see a list of available bots with numbers:
```
Available bots:
1. grn
2. dc
3. expense
4. quotation

Please text the number of the bot you want to chat with:
```

## Selecting a Bot
To select a bot, you can either:
1. Send the number corresponding to the bot:
   - Send "1" for grn bot
   - Send "2" for dc bot
   - Send "3" for expense bot
   - Send "4" for quotation bot
2. Send the name of the bot directly:
   - Send "grn" for grn bot
   - Send "dc" for dc bot
   - Send "expense" for expense bot
   - Send "quotation" for quotation bot

## During a Bot Session
Once you've selected a bot, you can interact with it normally. Numbers sent during a conversation will be forwarded to the bot as messages, not interpreted as bot switches.

For example, when chatting with the quotation bot, sending "2" will be sent to the quotation bot as a message, not switch you to the dc bot.

## Switching Bots
To switch to a different bot while in a session, use the `/switch` command followed by the bot number:
- `/switch 1` - Switch to grn bot
- `/switch 2` - Switch to dc bot
- `/switch 3` - Switch to expense bot
- `/switch 4` - Switch to quotation bot

## Other Commands
- `/bots` - Show the list of available bots again
- `/switch` - Show help for switching bots

## Examples
1. User: "hello"
   System: Shows bot list
   
2. User: "4"
   System: "You are now chatting with quotation bot. Send start!"
   
3. User: "2" (while in quotation bot session)
   System: Forwards "2" to quotation bot (does NOT switch bots)
   
4. User: "/switch 2"
   System: "You were chatting with quotation bot. Now you are chatting with dc bot. Send start!"

## Important Notes
- Numbers sent during a bot session are now ALWAYS forwarded to the bot as messages
- Bot switching now requires explicit use of the `/switch` command
- This change prevents accidental bot switching when sending numbers as part of a conversation