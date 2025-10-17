import asyncio
import httpx
from main import app
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)

def test_mr_bot_selection_by_name():
    """Test selecting the mr bot by name"""
    # Select the "mr" bot by name
    chat_data = {
        "user_id": "test_user",
        "message": "mr",
        "session_id": "test_session_mr"
    }
    
    response = client.post("/chatbot", json=chat_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "bot_name" in data
    assert data["bot_name"] == "mr"
    print(f"Successfully selected mr bot by name: {data['bot_name']}")

def test_mr_bot_selection_by_number():
    """Test selecting the mr bot by number"""
    # First, get the bot list to determine the number for "mr"
    response = client.get("/list_bots")
    bots = response.json()["available_bots"]
    mr_index = bots.index("mr") + 1  # 1-based indexing
    
    # Select the mr bot by number
    chat_data = {
        "user_id": "test_user",
        "message": str(mr_index),
        "session_id": "test_session_mr_2"
    }
    
    response = client.post("/chatbot", json=chat_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "bot_name" in data
    assert data["bot_name"] == "mr"
    print(f"Successfully selected mr bot by number: {data['bot_name']}")

if __name__ == "__main__":
    print("Testing mr bot selection functionality...")
    test_mr_bot_selection_by_name()
    test_mr_bot_selection_by_number()
    print("All mr bot tests passed!")