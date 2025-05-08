import cv2
import mediapipe as mp
import os

# Create output directory if it doesn't exist
output_dir = r"C:\Users\patha\Documents\9"
os.makedirs(output_dir, exist_ok=True)

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

num_imgs_taken = 0
element = 1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    result = hands.process(frame_rgb)
    frame_copy = frame.copy()

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_copy, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Bounding box around hand
            img_height, img_width, _ = frame.shape
            x_coords = [lm.x * img_width for lm in hand_landmarks.landmark]
            y_coords = [lm.y * img_height for lm in hand_landmarks.landmark]
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))

            # Expand the box a bit
            margin = 20
            x_min = max(0, x_min - margin)
            y_min = max(0, y_min - margin)
            x_max = min(img_width, x_max + margin)
            y_max = min(img_height, y_max + margin)

            # Extract and save the hand ROI
            hand_img = frame[y_min:y_max, x_min:x_max]
            if hand_img.size != 0 and num_imgs_taken <= 300:
                save_path = os.path.join(output_dir, f"{num_imgs_taken}.jpg")
                cv2.imwrite(save_path, hand_img)
                num_imgs_taken += 1
            elif num_imgs_taken > 300:
                break

            cv2.putText(frame_copy, f'{num_imgs_taken} images for {element}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    else:
        cv2.putText(frame_copy, 'No hand detected...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Hand Gesture Capture", frame_copy)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to break
        break

cap.release()
cv2.destroyAllWindows()
