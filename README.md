Omen's Ai
=========

A Python web app built to detect unusual network traffic patterns. It takes basic traffic metrics (bytes downloaded and login attempts) and runs them through an Isolation Forest model to flag anomalies. 

The backend runs on FastAPI, stores scan history in MongoDB Atlas, and is deployed with Docker on Render.

Live Demo
---------
https://omens-ai.onrender.com

Note: This runs on Render's free tier, so if nobody has opened the link in a while, the server takes about 50 seconds to wake up on the first visit.

Tech Stack
----------
- Python, FastAPI, Uvicorn
- scikit-learn & pandas (Isolation Forest model)
- MongoDB Atlas & PyMongo (scan history storage)
- HTML, CSS, Vanilla JS
- Docker & Render

Files in this Repo
------------------
- main.py - FastAPI server, anomaly detection model, and `/analyze` + `/history` routes.
- index.html - Web dashboard for testing traffic inputs.
- ai_monitor.py - Local monitoring script.
- requirements.txt - Python package list.
- Dockerfile - Container setup for Render.

Running Locally
---------------
1. Clone the repo:
   git clone https://github.com/anshveer11b/my-ai-project.git
   cd my-ai-project

2. Set up a virtual environment and install packages:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Add your MongoDB connection string (optional for local testing):
   Create a `.env` file in the root folder and add:
   MONGO_URI=your_mongodb_connection_string

4. Run the server:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload