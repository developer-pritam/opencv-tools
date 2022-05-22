import cv2
import mediapipe as mp
import time


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils



pTime = 0
Fingers = 0
cam = cv2.VideoCapture(0)

while True:

    success, img = cam.read()
    ImgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(ImgRGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)          
            
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime



    cv2.putText(img, f'Finger Count:- {int(Fingers)}', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 0, 255), 2)
    cv2.putText(img, f'FPS: {int(fps)}', (510, 450), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 0, 255), 2)
    cv2.putText(img, 'Pritam Kumar' , (10, 450), cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 0, 0), 2)

    cv2.imshow("Pritam Finger Count", img)
    cv2.waitKey(1)
