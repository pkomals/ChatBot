# Order Tracking Chatbot

## Directory Structure
```
backend/           
db/                
dialogflow_assets/ 
frontend/         
```

## Installation
### Install Required Modules
install all dependencies in one go using:
```bash
pip install -r backend/requirements.txt
```

## Running the FastAPI Backend Server
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## Setting Up Ngrok for HTTPS Tunneling
1. Download Ngrok from [ngrok.com/download](https://ngrok.com/download) and install the appropriate version for your OS.
2. Extract the downloaded ZIP file and place `ngrok.exe` in a preferred folder.
3. Open the command prompt, navigate to that folder, and run:
   ```bash
   ngrok http 8000
   ```
