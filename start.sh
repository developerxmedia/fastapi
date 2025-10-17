#!/bin/bash
# Go to project directory
cd /opt/aibots

# Activate the virtual environment
source venv/bin/activate

# Run FastAPI app
uvicorn main:app --host 0.0.0.0 --port 8001
