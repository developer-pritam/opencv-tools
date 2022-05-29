import cv2
import numpy as np
import mediapipe as mp
import time
import math

import autopy # Mouse pointer controller


def start(): 

    ##########################
    wCam, hCam = 640, 480  # Frame Size
    frameR = 100 # Frame Reduction
    smoothening = 10 
    #########################


    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)


    mpHands = mp.solutions.hands
    hands = mpHands.Hands( static_image_mode=True,max_num_hands=2,min_detection_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils 

    wScr, hScr = autopy.screen.size()

        
    while True:
    # 1. Find hand Landmarks
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect hands
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        lmList = [] # List of landmarks
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h) # Hand points coordinates
                    lmList.append([id, cx, cy])    
                    
                mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)

                # 2. Get the tip of the index and middle fingers
                if len(lmList) != 0:
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]

                    # 3. Check which fingers are up
                
                    tipIds = [4, 8, 12, 16, 20]
                    fingers = []
                    # Thumb
                    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
    
                    # Fingers
                    for id in range(1, 5):
                        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    print(fingers)


                    # 4. Only Index Finger : Moving Mode
                    if fingers[1] == 1 and fingers[2] == 0:
                    # 5. Convert Coordinates
                        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                    # 6. Smoothen Values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening
        
                    # 7. Move Mouse
                        autopy.mouse.move(wScr - clocX, clocY)
                        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY
            
                    # 8. Both Index and middle fingers are up : Clicking Mode
                    if fingers[1] == 1 and fingers[2] == 1:

                    # 9. Find distance between fingers

                        x1, y1 = lmList[8][1:]
                        x2, y2 = lmList[12][1:]
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    
                        length = math.hypot(x2 - x1, y2 - y1)
                        lineInfo = [x1, y1, x2, y2, cx, cy]
                        # print(length)

                    # 10. Click mouse if distance short
                        if length < 40:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                            autopy.mouse.click()


    # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "FPS: " + str(round(fps, 2)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)


        # 12. Display
        cv2.imshow("Mouse with hand guesture - Pritam", img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break