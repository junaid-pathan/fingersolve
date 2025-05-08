🖐️ FingerSolve
Solve Math Problems Using Hand Gestures!

FingerSolve is an interactive web app that turns simple math quizzes into a fun, hands-free experience. Powered by computer vision, OpenCV, MediaPipe, and a neural network, it recognizes your hand gestures in real-time through a webcam to evaluate your answers to math problems.

🚀 Features
🎥 Webcam-Based Input – Detects hand gestures using the webcam

🧠 Neural Network Model – Trained to recognize digits 0–9 from hand landmarks

🧮 Live Math Quizzes – Random addition or subtraction problems

🖐️ MediaPipe Landmarks – Used for accurate hand detection

⚙️ OpenCV + TensorFlow + Flask – Handles gesture processing and prediction

🎨 Modern UI – Built with React.js and Framer Motion

🛠️ Tech Stack
Frontend	Backend	ML / CV Tools
React.js	Flask (Python)	TensorFlow (Keras)
Tailwind CSS	REST API (JSON)	MediaPipe Hands
Framer Motion	Base64 image input	OpenCV + PIL

🧠 How It Works
A random math problem (like 3 + 2) is displayed.

You show the correct number of fingers in front of your webcam.

The app:

Captures the image frame

Extracts 21 hand landmarks using MediaPipe

Feeds the landmarks into a trained neural network

Predicts the digit and checks if it matches the correct answer

If correct ✅, your score increases and a new question appears!

📦 Installation
🔧 Backend (Flask + ML)
bash
Copy
Edit
git clone https://github.com/your-username/fingersolve.git
cd fingersolve/backend
pip install -r requirements.txt
python app.py
Make sure you have the trained model file finalmediapipe_landmarks_model.h5 in the backend folder.

🖥️ Frontend (React)
bash
Copy
Edit
cd ../frontend
npm install
npm run dev
Make sure your frontend is sending prediction requests to the Flask server (http://localhost:5000/predict).

🧪 Dataset & Model
Dataset: Custom dataset created using MediaPipe's 21-point hand landmarks

Features: 63 inputs (21 points × x, y, z)

Model: Dense Neural Network (Multi-Layer Perceptron)

Trained With: TensorFlow/Keras
