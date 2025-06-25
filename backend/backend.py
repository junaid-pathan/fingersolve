import base64
import io
import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import cv2
import mediapipe as mp
from flask import send_from_directory
app = Flask(__name__,static_folder='build', static_url_path='')
try:
    model = load_model("finalmediapipe_landmarks_model.h5")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

# Label map
labels_dict = {
    0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four',
    5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine'
}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')
@app.route('/quiz')
def quiz():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded properly'}), 500
        
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
            
        image_data = data['image']
        
        # Print the first 50 chars of the image data to verify format
        print(f"Received image data (first 50 chars): {image_data[:50]}...")
        
        try:
            # Decode base64 image
            # Handle different formats of base64 data
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            image_np = np.array(image)
            
            # Print image shape for debugging
            print(f"Image shape: {image_np.shape}")
            
            # Convert to RGB format for MediaPipe
            results = hands.process(image_np)

            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0]
                # Extract 21 landmarks × 3 coordinates = 63 features
                features = []
                for lm in landmarks.landmark:
                    features.extend([lm.x, lm.y, lm.z])
                
                if len(features) != 63:
                    print(f"Warning: Expected 63 features, got {len(features)}")
                
                input_data = np.array(features).reshape(1, -1)

                # Predict
                prediction = model.predict(input_data)
                pred_class = np.argmax(prediction)
                predicted_label = labels_dict[pred_class]
                confidence = float(prediction[0][pred_class])
                
                print(f"Prediction: {predicted_label} with confidence {confidence:.4f}")
                
                return jsonify({
                    'prediction': predicted_label,
                    'confidence': confidence
                })
            else:
                print("No hand detected in the image")
                return jsonify({'prediction': 'NoHand'})
                
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple endpoint to verify server is running"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)