import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
from sklearn.ensemble import IsolationForest
from pymongo import MongoClient
from dotenv import load_dotenv

# Load secret environment variables (if running locally with a .env file)
load_dotenv()

app = FastAPI(title="AI Cyber Cell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MONGODB DATABASE SETUP ---
MONGO_URI = os.getenv("MONGO_URI")
logs_collection = None

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI)
        db = client["omens_ai_db"]
        logs_collection = db["traffic_logs"]
        print("✅ Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"⚠️ MongoDB connection error: {e}")
else:
    print("⚠️ MONGO_URI not set. Running without database memory.")

# --- TRAIN AI MODEL ---
baseline_data = {
    'Bytes_Downloaded': [1200, 1500, 1100, 1300, 1400, 1250, 1450, 1600],
    'Login_Attempts': [1, 2, 1, 1, 2, 1, 3, 1]
}
df = pd.DataFrame(baseline_data)
ai_model = IsolationForest(contamination=0.1, random_state=42)
ai_model.fit(df)

class NetworkTraffic(BaseModel):
    bytes_downloaded: int
    login_attempts: int

@app.get("/")
def serve_dashboard():
    return FileResponse("index.html")

@app.post("/analyze")
def analyze_traffic(traffic: NetworkTraffic):
    new_data = pd.DataFrame({
        'Bytes_Downloaded': [traffic.bytes_downloaded],
        'Login_Attempts': [traffic.login_attempts]
    })
    prediction = ai_model.predict(new_data)
    
    status = "🚨 ALERT! Anomaly Detected!" if prediction[0] == -1 else "✅ Normal"
    
    # Save prediction to MongoDB memory
    if logs_collection is not None:
        log_entry = {
            "bytes_downloaded": traffic.bytes_downloaded,
            "login_attempts": traffic.login_attempts,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logs_collection.insert_one(log_entry)
        print(f"💾 Saved log to MongoDB: {log_entry}")
        
    return {"status": status, "data": traffic}

# NEW: View the last 50 saved AI predictions from MongoDB!
@app.get("/history")
def get_traffic_history():
    if logs_collection is None:
        return {"error": "Database not connected yet. Check MONGO_URI on Render."}
    
    # Fetch newest logs first, hiding MongoDB's internal '_id' field
    logs = list(logs_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(50))
    return {"total_saved": len(logs), "history": logs}