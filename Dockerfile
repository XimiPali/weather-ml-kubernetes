FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY requirements.txt .
COPY app.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Telling Docker this container listens on port 5000
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
