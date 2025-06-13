# Use the official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract OCR engine
RUN apt-get update && apt-get install -y tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Copy all project files into the container
COPY . .

# Expose the port your app runs on (adjust if needed)
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
