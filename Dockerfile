FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Create data dir
RUN mkdir -p data

# Run the bot
CMD ["python", "bot/main.py"]
