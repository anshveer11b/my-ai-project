import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Create a dataset of "Network Traffic"
# Let's say this is [Bytes_Downloaded, Login_Attempts_Per_Minute]
data = {
    'Bytes_Downloaded': [1200, 1500, 1100, 1300, 1400, 95000, 1250, 1450, 1600],
    'Login_Attempts': [1, 2, 1, 1, 2, 45, 1, 3, 1]
}

# Convert it into a table (DataFrame)
df = pd.DataFrame(data)
print("--- Network Log Data ---")
print(df)
print("\n")

# 2. Build the AI Model
# contamination=0.1 means we guess about 10% of our data might be malicious
ai_model = IsolationForest(contamination=0.2, random_state=42)

# 3. Train the AI (Show it the data)
ai_model.fit(df)

# 4. Ask the AI to predict which traffic is an anomaly
# It returns 1 for Normal, and -1 for Anomaly
df['Threat_Score'] = ai_model.predict(df[['Bytes_Downloaded', 'Login_Attempts']])

# 5. Review the Results
print("--- AI Threat Analysis ---")
for index, row in df.iterrows():
    if row['Threat_Score'] == -1:
        print(f"🚨 ALERT! Anomaly Detected at row {index}: {row['Bytes_Downloaded']} bytes, {row['Login_Attempts']} logins.")
    else:
        print(f"✅ Normal: Row {index}")