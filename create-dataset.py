import mediapipe as mp
import cv2
import os
import pickle
import matplotlib.pyplot as plt

# objects to draw the landmarks and detect them
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = "./data"

data = []
labels = []  # categories for each one of these points

for dirName in os.listdir(DATA_DIR):
    for imgPath in os.listdir(os.path.join(DATA_DIR, dirName)):
        data_aux = []
        img = cv2.imread(os.path.join(DATA_DIR, dirName, imgPath))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)  # detecting all landmarks in this image
        if results.multi_hand_landmarks:  # all landmarks
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)
            data.append(data_aux)
            labels.append(dirName)

f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
