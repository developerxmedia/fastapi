import asyncio
import httpx
from main import app
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)

def test_list_bots():
    """Test the list_bots endpoint"""
    response = client.get("/list_bots")
    assert response.status_code == 200
    data = response.json()
    assert "available_bots" in data
    assert len(data["available_bots"]) > 0
    print("Available bots:", data["available_bots"])

def test_bot_selection_by_number():
    """Test selecting a bot by number"""
    # First, get the bot list
    response = client.get("/list_bots")
    bots = response.json()["available_bots"]
    
    # Select the first bot by number (1)
    chat_data = {
        "user_id": "test_user",
        "message": "1",
        "session_id": "test_session_1"
    }
    
    response = client.post("/chatbot", json=chat_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "bot_name" in data
    assert data["bot_name"] == bots[0]  # Should be the first bot
    print(f"Successfully selected bot by number: {data['bot_name']}")

def test_bot_selection_by_name():
    """Test selecting a bot by name"""
    # Select the "dc" bot by name
    chat_data = {
        "user_id": "test_user",
        "message": "dc",
        "session_id": "test_session_2"
    }
    
    response = client.post("/chatbot", json=chat_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "bot_name" in data
    assert data["bot_name"] == "dc"
    print(f"Successfully selected bot by name: {data['bot_name']}")

def test_invalid_bot_selection():
    """Test invalid bot selection"""
    # Try to select an invalid bot
    chat_data = {
        "user_id": "test_user",
        "message": "invalid_bot",
        "session_id": "test_session_3"
    }
    
    response = client.post("/chatbot", json=chat_data)
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    print(f"Correctly handled invalid bot selection: {data['error']}")

if __name__ == "__main__":
    print("Testing bot selection functionality...")
    test_list_bots()
    test_bot_selection_by_number()
    test_bot_selection_by_name()
    test_invalid_bot_selection()
    print("All tests passed!")