import cv2
import mediapipe as mp
import pickle
import numpy as np
import time

modelDict = pickle.load(open('./model.p', 'rb'))
model = modelDict['model']


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'N', 1: 'I', 2: 'H', 3: 'A', 4: 'L'}

# to build sentence on screen
sentence = ""
last_char = None
char_start_time = 0
LETTER_HOLD_SEC = 5

cv2.resizeWindow('frame', 200, 600)  # set window width and height

while True:
    data_aux = []
    xDup = []
    yDup = []
    ret, frame = cap.read()
    H, W, _ = frame.shape  # ignore the number of color channels

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)  # detecting all landmarks in this image
    if results.multi_hand_landmarks:  # all landmarks

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
                xDup.append(x)
                yDup.append(y)

        # setting dimensions for the square
        x1 = int(min(xDup) * W) - 10
        y1 = int(min(yDup) * H) - 10

        x2 = int(max(xDup) * W) - 10
        y2 = int(max(yDup) * H) - 10

        prediction = model.predict([np.asarray(data_aux)])
        predictedChar = labels_dict[int(prediction[0])]

        # sentence building
        now = time.time()
        if predictedChar == last_char:
            # if holding same sign for 5 sec - add sentence
            if now - char_start_time >= LETTER_HOLD_SEC:
                sentence += predictedChar
                #reset timer once letter added
                char_start_time = now  
        else:
            # New sign detected - start timer
            last_char = predictedChar
            char_start_time = now

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)  # dimensions, color, width
        cv2.putText(frame, predictedChar, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)
    
    # display the sentence at the top of the frame
    cv2.putText(frame, f"Sentence: {sentence}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3, cv2.LINE_AA)
    
    cv2.imshow('frame', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Quit
        break
    elif key == ord('c'):  # Clear sentence
        sentence = ""

cap.release()
cv2.destroyAllWindows()
