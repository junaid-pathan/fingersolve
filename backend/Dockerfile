# Use Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies for mediapipe & opencv
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy backend app code
COPY backend/ .

# Expose the port Flask runs on
EXPOSE 5000

# Start the Flask app
CMD ["gunicorn", "backend:app", "--bind", "0.0.0.0:5000"]
