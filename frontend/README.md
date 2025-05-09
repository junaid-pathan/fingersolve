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

```bash
$ git clone https://github.com/yourusername/fingersolve.git
$ cd fingersolve
$ python app.py
```

NOTE: USE A VIRTUAL ENVIRONMENT TO RUN THE TENSORFLOW MODULE AS NEW VERSION OF PYTHON DOESN'T HAVE IT.
For that : 

```bash
Windows
python3.11 -m venv venv
venv\Scripts\activate.bat

Mac
python3.11 -m venv venv
source venv/bin/activate

To install all the dependencies: 
pip install -r requirements.txt
```

Make sure you have the trained model file finalmediapipe_landmarks_model.h5 in the backend folder.

🖥️ Frontend (React)
```bash 
cd ../frontend
npm install
npm run dev
```
Make sure your frontend is sending prediction requests to the Flask server (http://localhost:5000/predict).




