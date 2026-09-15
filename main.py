from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # NEW: Allows sending files
from pydantic import BaseModel
import pandas as pd
from sklearn.ensemble import IsolationForest

app = FastAPI(title="AI Cyber Cell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Train AI Model
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

# NEW: When someone visits the main URL, show them the dashboard!
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
    
    if prediction[0] == -1:
        return {"status": "🚨 ALERT! Anomaly Detected!", "data": traffic}
    else:
        return {"status": "✅ Normal", "data": traffic}