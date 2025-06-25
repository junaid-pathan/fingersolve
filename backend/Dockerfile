# Use Python 3.10 base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Install system-level dependencies for MediaPipe and OpenCV
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the backend code into the container
COPY . .

# Expose Flask port
EXPOSE 5000

# Start the app using Gunicorn
CMD ["gunicorn", "backend:app", "--bind", "0.0.0.0:5000"]
