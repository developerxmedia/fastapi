# Multi-Bot Gateway

A FastAPI-based gateway that allows users to interact with multiple bots through a single interface.

## Overview

This gateway service provides a unified interface for communicating with various specialized bots:
- GRN Bot
- DC Bot
- Expense Bot
- Quotation Bot
- MR Bot

Users can select a bot to chat with and maintain a session with that bot until they choose to switch.

## Features

- List available bots
- Select a bot to chat with
- Maintain session with selected bot
- Switch between bots by explicitly requesting bot list first
- Handle both text messages and base64 encoded images
- Session-based bot selection (each session_id maintains independent bot selection)

## Usage

### Initial Interaction
When a user first sends a message (like "hello"), they will see a list of available bots with numbers:
```
Available bots:
1. grn
2. dc
3. expense
4. quotation
5. mr

Please text the number of the bot you want to chat with:
```

### Selecting a Bot
To select a bot, you can either:
1. Send the number corresponding to the bot:
   - Send "1" for grn bot
   - Send "2" for dc bot
   - Send "3" for expense bot
   - Send "4" for quotation bot
   - Send "5" for mr bot
2. Send the name of the bot directly:
   - Send "grn" for grn bot
   - Send "dc" for dc bot
   - Send "expense" for expense bot
   - Send "quotation" for quotation bot
   - Send "mr" for mr bot

### During a Bot Session
Once you've selected a bot, you can interact with it normally. Numbers sent during a conversation (such as product selection) will be forwarded to the bot as part of the conversation.

To switch to a different bot:
1. Send "/bots", "bots", or "list" to see the available bots
2. Send the number of the bot you want to switch to

### Session Management
- Each session is identified by a unique `session_id`
- Different sessions can have different bots selected
- When a new session is started (new `session_id`), it begins with no bot selected
- Sessions are independent of each other

### Other Commands
- `/bots`, `bots`, or `list` - Show the list of available bots again and reset the current session

## API Endpoints

- `POST /chatbot` - Main endpoint for chat interactions
- `GET /list_bots` - List all available bots
- `GET /current_bot/{user_id}` - Get current bot for a user (deprecated)
- `GET /current_bot_by_session/{session_id}` - Get current bot for a session
- `POST /change_bot` - Programmatically change a session's bot
- `POST /logout` - End a session's bot session

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

## Recent Changes

### Product Selection Fix (September 2025)
Fixed an issue where numbers sent during product selection in the quotation bot were incorrectly interpreted as bot switching commands.

**Before:** Sending "1" during product selection would switch to the grn bot.
**After:** Sending "1" during product selection correctly selects the first product.

See [PRODUCT_SELECTION_FIX.md](PRODUCT_SELECTION_FIX.md) for details.

### Bot Switching Behavior Update (September 2025)
Simplified bot switching to make it more intuitive:
- Users can now switch bots by requesting the bot list and then sending a number
- The `/bots` command automatically resets the session and shows the bot list
- Removed the need for the `/switch` command

See [BOT_SWITCHING_BEHAVIOR_UPDATE.md](BOT_SWITCHING_BEHAVIOR_UPDATE.md) for details.

### Session-Based Bot Selection (September 2025)
Changed bot selection tracking from user-based to session-based:
- Each session (identified by `session_id`) now maintains independent bot selection
- New sessions start fresh without any bot pre-selected
- Multiple concurrent sessions can have different bots selected

See [SESSION_BASED_BOT_SELECTION.md](SESSION_BASED_BOT_SELECTION.md) for details.

### Bot Switching Fix (September 2025)
Fixed an issue where numbers sent during a bot session were incorrectly interpreted as bot switching commands. 

**Before:** Sending "2" while chatting with the quotation bot would switch to the dc bot.
**After:** Sending "2" while chatting with the quotation bot forwards "2" as a message to the quotation bot.

Users must now explicitly use the `/switch [number]` command to switch bots.

See [BOT_SWITCHING_FIX_SUMMARY.md](BOT_SWITCHING_FIX_SUMMARY.md) for details.