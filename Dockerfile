# 1. Use an official, lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your files (main.py, index.html)
COPY . .

# 5. Tell the cloud which port to open
EXPOSE 8000

# 6. The command to start your AI Server in the cloud
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]