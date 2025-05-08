import os
import cv2
import numpy as np
import mediapipe as mp
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

# Define MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Update paths
data_path = r'C:\Users\patha\Downloads\sign-language-recognition-project\code\gesture\train'
model_save_path = r'C:\Users\patha\Downloads\sign-language-recognition-project\code\finalmediapipe_landmarks_model.h5'

# Prepare data
X = []
y = []
labels_dict = {}
label_idx = 0

for label_name in os.listdir(data_path):
    label_folder = os.path.join(data_path, label_name)
    if not os.path.isdir(label_folder): continue

    if label_name not in labels_dict:
        labels_dict[label_name] = label_idx
        label_idx += 1

    for img_file in os.listdir(label_folder):
        img_path = os.path.join(label_folder, img_file)
        img = cv2.imread(img_path)
        if img is None: continue
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = hands.process(img_rgb)
        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            X.append(landmarks)
            y.append(labels_dict[label_name])

hands.close()

X = np.array(X)
y = to_categorical(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model definition
model = Sequential([
    Dense(128, activation='relu', input_shape=(63,)),
    Dropout(0.4),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(y.shape[1], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=1, min_lr=0.0001)
early_stop = EarlyStopping(monitor='val_loss', patience=3)

# Train model
history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
                    epochs=20, batch_size=16, callbacks=[reduce_lr, early_stop])

# Evaluate
scores = model.evaluate(X_test, y_test, verbose=0)
print(f'\nLoss: {scores[0]:.4f} | Accuracy: {scores[1]*100:.2f}%')

# Save model
model.save(model_save_path)
print(f'\n✅ Model saved to: {model_save_path}')
