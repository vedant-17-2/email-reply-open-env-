FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY . .

# HF Spaces uses port 7860
EXPOSE 7860

# Start the server
CMD ["python", "main.py"]
