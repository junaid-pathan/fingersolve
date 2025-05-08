import cv2
import numpy as np
import keras
import mediapipe as mp
import time

# Load model and label map
model_path = "finalmediapipe_landmarks_model.h5"
try:
    model = keras.models.load_model(model_path)
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Map indices back to labels
labels_dict = {
    0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four',
    5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine'
}

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, 
                      min_detection_confidence=0.7, 
                      min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Custom drawing specs for better visualization
hand_landmark_drawing_spec = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
hand_connection_drawing_spec = mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2)

# Initialize webcam
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Error: Could not open webcam")
    exit(1)

# Set camera resolution for better performance
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variables for smoothing predictions
prediction_history = []
history_length = 5
last_prediction_time = time.time()
current_prediction = None
confidence = 0

# Function to draw a nice-looking prediction box
def draw_prediction_box(frame, label, confidence, x, y, width=200, height=80):
    # Draw background rectangle
    cv2.rectangle(frame, (x, y), (x + width, y + height), (50, 50, 50), -1)
    cv2.rectangle(frame, (x, y), (x + width, y + height), (100, 100, 100), 2)
    
    # Draw label text
    cv2.putText(frame, f"Prediction: {label}", (x + 10, y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Draw confidence bar
    bar_width = int((width - 20) * confidence)
    cv2.rectangle(frame, (x + 10, y + 45), (x + 10 + bar_width, y + 60), 
                 (0, 255, 0) if confidence > 0.7 else (0, 255, 255) if confidence > 0.5 else (0, 0, 255), -1)
    cv2.rectangle(frame, (x + 10, y + 45), (x + width - 10, y + 60), (200, 200, 200), 1)
    
    # Draw confidence percentage
    cv2.putText(frame, f"{confidence*100:.1f}%", (x + width - 60, y + 57),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# Main loop
print("Starting gesture recognition. Press ESC to exit.")
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Flip the frame horizontally for a more intuitive mirror view
    frame = cv2.flip(frame, 1)
    
    # Create a copy for drawing
    display_frame = frame.copy()
    
    # Convert to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with MediaPipe
    result = hands.process(frame_rgb)

    # Draw title and instructions
    cv2.putText(display_frame, "Sign Language Translator", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 120, 255), 2)
    cv2.putText(display_frame, "Show a number from 0-9 with your hand", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 200), 1)
    
    # Check if hand is detected
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks with custom style
            mp_draw.draw_landmarks(
                display_frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=hand_landmark_drawing_spec,
                connection_drawing_spec=hand_connection_drawing_spec
            )

            # Extract landmark coordinates
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # Make prediction
            try:
                input_data = np.array(landmarks).reshape(1, -1)
                prediction = model.predict(input_data, verbose=0)
                pred_class = np.argmax(prediction)
                confidence_score = float(prediction[0][pred_class])
                
                # Add to prediction history for smoothing
                prediction_history.append((pred_class, confidence_score))
                if len(prediction_history) > history_length:
                    prediction_history.pop(0)
                
                # Get most common prediction from history
                pred_counts = {}
                conf_sums = {}
                for p, c in prediction_history:
                    pred_counts[p] = pred_counts.get(p, 0) + 1
                    conf_sums[p] = conf_sums.get(p, 0) + c
                
                # Find the most frequent prediction
                most_common = max(pred_counts.items(), key=lambda x: x[1])
                most_common_class = most_common[0]
                avg_confidence = conf_sums[most_common_class] / most_common[1]
                
                # Update current prediction if it's stable
                if time.time() - last_prediction_time > 0.5:  # Update every 0.5 seconds
                    current_prediction = labels_dict[most_common_class]
                    confidence = avg_confidence
                    last_prediction_time = time.time()
                    #for the fron
                
            except Exception as e:
                print(f"Prediction error: {e}")
                current_prediction = "Error"
                confidence = 0
    else:
        # If no hand is detected
        cv2.putText(display_frame, "No hand detected", (10, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Clear prediction history when no hand is detected
        prediction_history = []
        if time.time() - last_prediction_time > 1.0:
            current_prediction = None
    
    # Draw the prediction box
    if current_prediction:
        draw_prediction_box(display_frame, current_prediction, confidence, 
                           x=display_frame.shape[1] - 220, y=20)
        
        # Draw large number in the corner for clear visibility
        number_text = current_prediction.split()[-1]  # Extract just the number part
        cv2.putText(display_frame, number_text, 
                   (display_frame.shape[1] - 120, display_frame.shape[0] - 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
    
    # Add FPS counter
    fps = cam.get(cv2.CAP_PROP_FPS)
    cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, display_frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Show the frame
    cv2.imshow("Hand Gesture Recognition", display_frame)

    # Check for ESC key to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Clean up
print("Closing application...")
cam.release()
cv2.destroyAllWindows()
hands.close()
print("Application closed successfully")