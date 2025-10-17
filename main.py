# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Union
import httpx
from config import BOT_ENDPOINTS
from sessions import set_session_bot, get_session_bot, clear_session_bot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Multi Bot Gateway")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Or restrict to specific domains like ["http://localhost:3000", "https://yourapp.com"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

class ChatRequest(BaseModel):
    user_id: Union[str, int]
    message: Optional[str] = ""
    action: Optional[str] = "general_chat"
    session_id: Optional[str] = ""
    image: Optional[str] = ""
    voice: Optional[str] = ""


@app.get("/list_bots")
async def list_bots():
    return {"available_bots": list(BOT_ENDPOINTS.keys())}


@app.post("/chatbot")
async def chatbot(request: ChatRequest):
    """
    Main endpoint for mobile app - handles both text messages and base64 image data.
    Either message or image must be provided, but not both.
    If user hasn't selected a bot yet, shows bot list.
    If message is a number, selects that bot.
    Otherwise forwards message or image to selected bot.
    """
    user_id = str(request.user_id)
    message = request.message or ""
    image_base64 = request.image or ""
    session_id = request.session_id or ""
    action = request.action or "general_chat"

    # Check if user wants to see bots again
    if message.strip().lower() in ["/bots", "bots", "list"]:
        bots = list(BOT_ENDPOINTS.keys())
        message_text = "Available bots:\n"
        for i, bot in enumerate(bots, 1):
            message_text += f"{i}. {bot}\n"
        message_text += "\nPlease text the number of the bot you want to chat with:"
        
        # Clear session when user requests to see bots again
        if session_id:
            clear_session_bot(session_id)
            
        return {"user_id": user_id, "message": message_text}
        
    # Check if user has already selected a bot
    bot_name = get_session_bot(session_id) if session_id else None

    # If no bot selected yet, handle bot selection
    if not bot_name:
        if not message and not image_base64:
            bots = list(BOT_ENDPOINTS.keys())
            message_text = "Available bots:\n"
            for i, bot in enumerate(bots, 1):
                message_text += f"{i}. {bot}\n"
            message_text += "\nPlease text the number of the bot you want to chat with:"
            return {"user_id": user_id, "message": message_text}

        if message:
            bots = list(BOT_ENDPOINTS.keys())
            message_stripped = message.strip()
            
            # Try to select bot by number first
            try:
                bot_index = int(message_stripped)
                if 1 <= bot_index <= len(bots):
                    bot_name = bots[bot_index - 1]
                    # Clear any existing session for this session before setting new bot
                    if session_id:
                        clear_session_bot(session_id)
                    # Set the new bot for this session
                    if session_id:
                        set_session_bot(session_id, bot_name)
                    return {
                        "user_id": user_id,
                        "message": f"You are now chatting with {bot_name} bot. Send start!",
                        "bot_name": bot_name,
                    }
                else:
                    message_text = "Available bots:\n"
                    for i, bot in enumerate(bots, 1):
                        message_text += f"{i}. {bot}\n"
                    message_text += f"\nPlease enter a number between 1 and {len(bots)} or type the bot name:"
                    return {
                        "user_id": user_id,
                        "message": message_text,
                        "error": f"Please enter a number between 1 and {len(bots)} or type the bot name.",
                    }
            except ValueError:
                # If not a number, try to select bot by name
                if message_stripped in BOT_ENDPOINTS:
                    bot_name = message_stripped
                    # Clear any existing session for this session before setting new bot
                    if session_id:
                        clear_session_bot(session_id)
                    # Set the new bot for this session
                    if session_id:
                        set_session_bot(session_id, bot_name)
                    return {
                        "user_id": user_id,
                        "message": f"You are now chatting with {bot_name} bot. Send start!",
                        "bot_name": bot_name,
                    }
                else:
                    message_text = "Available bots:\n"
                    for i, bot in enumerate(bots, 1):
                        message_text += f"{i}. {bot}\n"
                    message_text += "\nPlease enter a number or type the bot name you want to chat with:"
                    return {
                        "user_id": user_id,
                        "message": message_text,
                        "error": "Please enter a valid number or bot name.",
                    }
        else:
            bots = list(BOT_ENDPOINTS.keys())
            message_text = "Available bots:\n"
            for i, bot in enumerate(bots, 1):
                message_text += f"{i}. {bot}\n"
            message_text += "\nPlease select a bot first by sending a number or bot name:"
            return {
                "user_id": user_id,
                "message": message_text,
                "error": "Please select a bot first by sending a number or bot name.",
            }
    else:
        # Session has already selected a bot
        # Forward all messages to the bot (no automatic bot switching with numbers)
        # Bot switching will only happen if user explicitly requests bot list first
        pass

    # Session has selected a bot, forward message or image to the bot
    bot_url = BOT_ENDPOINTS[bot_name]
    # bot_data = {
    #     "user_id": int(user_id) if user_id.isdigit() else user_id,
    #     "session_id": session_id,
    # }
    bot_data = {
        "user_id": str(user_id),  # Always send as string to match direct calls
        "session_id": session_id,
        "image": "",  # Always include empty image field
        "voice": request.voice or "",  # Include voice parameter
    }

    # Determine the correct endpoint for each bot
    if bot_name == "dc":
        endpoint = "/dcchat"
    elif bot_name == "grn":
        endpoint = "/grnchat"
    elif bot_name == "expense":
        endpoint = "/expensechat"  # Correct endpoint for expense bot
    elif bot_name == "quotation":
        endpoint = "/chat"  # Correct endpoint for quotation bot
    elif bot_name == "mr":
        endpoint = "/mrchat"  # Correct endpoint for mr bot
    else:
        endpoint = "/process"  # Default endpoint for any other bots

    # Handle base64 image
    if image_base64:
        bot_data["action"] = "process_image"
        bot_data["image"] = image_base64
        bot_data["message"] = ""

        try:
            # Use a longer timeout for image processing (2 minutes) since it may take more time
            async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
                response = await client.post(f"{bot_url}{endpoint}", json=bot_data)
            
            # Check if response is empty or has no content
            if not response.content or len(response.content) == 0:
                return {
                    "user_id": user_id,
                    "message": "Image processed successfully by the bot.",
                    "note": "Bot returned no response content."
                }
            
            # Try to parse JSON response
            try:
                json_response = response.json()
                # Check if response is null or empty
                if json_response is None:
                    return {
                        "user_id": user_id,
                        "message": "Image processed successfully by the bot.",
                        "note": "Bot returned null response."
                    }
                elif isinstance(json_response, dict) and len(json_response) == 0:
                    return {
                        "user_id": user_id,
                        "message": "Image processed successfully by the bot.",
                        "note": "Bot returned empty response."
                    }
                return json_response
            except Exception as json_error:
                # If JSON parsing fails, return the raw text content
                try:
                    text_response = response.text
                    if not text_response or text_response.strip() == "":
                        return {
                            "user_id": user_id,
                            "message": "Image processed successfully by the bot.",
                            "note": "Bot returned empty text response."
                        }
                    else:
                        return {
                            "user_id": user_id,
                            "message": f"Bot returned non-JSON response: {text_response[:100]}{'...' if len(text_response) > 100 else ''}",
                            "note": "Raw response from bot provided above."
                        }
                except:
                    return {
                        "user_id": user_id,
                        "message": "Image processed successfully by the bot.",
                        "note": "Bot returned response in unknown format."
                    }
        except httpx.ReadTimeout:
            # Log timeout for debugging purposes
            print(f"Timeout occurred when contacting bot {bot_name} at {bot_url}{endpoint}")
            return {
                "user_id": user_id,
                "message": f"Bot {bot_name} took too long to respond. Please try again later.",
                "error": "Timeout",
            }
        except Exception as e:
            # Log other exceptions for debugging purposes
            print(f"Error occurred when contacting bot {bot_name} at {bot_url}{endpoint}: {str(e)}")
            # Also catch any other timeout-related exceptions
            if "timeout" in str(e).lower():
                return {
                    "user_id": user_id,
                    "message": f"Bot {bot_name} took too long to respond. Please try again later.",
                    "error": "Timeout",
                }
            return {
                "user_id": user_id,
                "message": f"Error while contacting {bot_name}.",
                "error": str(e),
            }

    # Handle text message
    elif message:
        if bot_name in ["dc", "grn"]:
            bot_data["action"] = "general_chat"
        elif bot_name == "quotation":
            bot_data["action"] = action
        elif bot_name == "mr":
            bot_data["action"] = "general_message"
        else:
            bot_data["action"] = "general_message"

        bot_data["message"] = message

        try:
            print(f"=== DEBUGGING AIBOT REQUEST ===")
            print(f"Bot name: {bot_name}")
            print(f"Bot URL: {bot_url}")
            print(f"Endpoint: {endpoint}")
            print(f"Full URL: {bot_url}{endpoint}")
            print(f"Request data: {bot_data}")
            print(f"Original action: {action}")
            print("================================")
            async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
                response = await client.post(f"{bot_url}{endpoint}", json=bot_data)
            
            # Check if response is empty or has no content
            if not response.content or len(response.content) == 0:
                return {
                    "user_id": user_id,
                    "message": "Message processed successfully by the bot.",
                    "note": "Bot returned no response content."
                }
            print(f"=== RESPONSE DEBUG ===")
            print(f"Status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response text: {response.text}")
            print("=====================")
            # Try to parse JSON response
            try:
                json_response = response.json()
                # Check if response is null or empty
                if json_response is None:
                    return {
                        "user_id": user_id,
                        "message": "Message processed successfully by the bot.",
                        "note": "Bot returned null response."
                    }
                elif isinstance(json_response, dict) and len(json_response) == 0:
                    return {
                        "user_id": user_id,
                        "message": "Message processed successfully by the bot.",
                        "note": "Bot returned empty response."
                    }
                return json_response
            except Exception as json_error:
                # If JSON parsing fails, return the raw text content
                try:
                    text_response = response.text
                    if not text_response or text_response.strip() == "":
                        return {
                            "user_id": user_id,
                            "message": "Message processed successfully by the bot.",
                            "note": "Bot returned empty text response."
                        }
                    else:
                        return {
                            "user_id": user_id,
                            "message": f"Bot returned non-JSON response: {text_response[:100]}{'...' if len(text_response) > 100 else ''}",
                            "note": "Raw response from bot provided above."
                        }
                except:
                    return {
                        "user_id": user_id,
                        "message": "Message processed successfully by the bot.",
                        "note": "Bot returned response in unknown format."
                    }
        except httpx.ReadTimeout:
            # Log timeout for debugging purposes
            print(f"Timeout occurred when contacting bot {bot_name} at {bot_url}{endpoint}")
            return {
                "user_id": user_id,
                "message": f"Bot {bot_name} took too long to respond. Please try again later.",
                "error": "Timeout",
            }
        except Exception as e:
            # Log other exceptions for debugging purposes
            print(f"Error occurred when contacting bot {bot_name} at {bot_url}{endpoint}: {str(e)}")
            # Also catch any other timeout-related exceptions
            if "timeout" in str(e).lower():
                return {
                    "user_id": user_id,
                    "message": f"Bot {bot_name} took too long to respond. Please try again later.",
                    "error": "Timeout",
                }
            return {
                "user_id": user_id,
                "message": f"Error while contacting {bot_name}.",
                "error": str(e),
            }

    # Neither message nor image
    return {
        "user_id": user_id,
        "message": "Please provide either a text message or an image in base64 format.",
        "error": "No message or image provided.",
    }


@app.get("/current_bot/{user_id}")
async def current_bot(user_id: str):
    # This endpoint is kept for backward compatibility but will need session_id to work properly
    return {"message": "Please provide session_id to get current bot information"}

@app.get("/current_bot_by_session/{session_id}")
async def current_bot_by_session(session_id: str):
    bot_name = get_session_bot(session_id)
    if not bot_name:
        return {"message": "No bot selected yet for this session"}
    return {"session_id": session_id, "current_bot": bot_name}


@app.post("/change_bot")
async def change_bot(request: Request):
    data = await request.json()
    session_id = data.get("session_id")
    new_bot = data.get("bot_name")

    if not session_id or new_bot not in BOT_ENDPOINTS:
        return {"error": "Invalid session_id or bot_name"}

    # Clear any existing session for this session before setting new bot
    clear_session_bot(session_id)
    # Set the new bot for this session
    set_session_bot(session_id, new_bot)
    return {"message": f"Bot changed successfully. Now chatting with {new_bot}"}


@app.post("/logout")
async def logout(request: Request):
    data = await request.json()
    session_id = data.get("session_id")

    if not session_id:
        return {"error": "session_id required"}

    clear_session_bot(session_id)
    return {"message": "You have logged out from your bot session"}

