This project uses MediaPipe hand tracking and a neural network to classify American Sign Language (ASL) hand signs from a webcam video feed.

## Features

- Real-time hand tracking using **MediaPipe**
- Hand sign classification using a trained **TensorFlow** model
- Custom model trained on extracted hand landmarks (63 features)
- Supports one-hot encoded label training with image folders

## Requirements

- Python **3.11**
- pip (Python package installer)
- A webcam (for real-time detection)

## Setup Instructions


```bash
git clone https://github.com/junaid-pathan/signlanguage.git
cd signlanguage

If you do not have 3.11, create a virtual environment using this in your command prompt
# Linux/macOS
python3.11 -m venv venv
source venv/bin/activate

# Windows
python3.11 -m venv venv
venv\Scripts\activate


DOWNLOAD ALL THE REQUIRED PACKAGES BY RUNNING : pip install -r requirements.txt

FINALLY RUN THE modeL_for_gesture.py
