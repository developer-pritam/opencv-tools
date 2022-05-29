import cv2
import mediapipe as mp # Media pipe by google for hand tracking

# Importing utility packages
import time
import math
import numpy as np

# Importing libraries for volume control
from ctypes import cast, POINTER    # To use .c functions
from comtypes import CLSCTX_ALL     # To use dispact based function like DLL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # To use volume control
# Pycaw source https://github.com/AndreMiras/pycaw


def start():

    # Import the mediapipe/python/hand_tracking/ and drawing module
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils


    # Getting the volume control object
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # print(volume.GetVolumeRange()) checked volume range

    minVol = -65 # Minimum volume level
    maxVol = 0 # Maximum volume level
    currentVol = 0 # Current volume level
    volumeBarMax = 350 # Volume bar size maxium
    volumeBarMin = 200 # Volume bar size minimum
    volumePer = 0 # Volume percentage 
    volumeBar = 350 # current Volume bar value 


    # Accessing  camera 0
    cap = cv2.VideoCapture(0)

    # Current time and previous time for calculating fps 
    pTime = 0
    cTime = 0
    length =0

    handRangeMin = 50 # Minimum hand range
    handRangeMax = 180 # Maximum hand range

    while True:

        # Capture frame-by-frame
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

                if len(lmList) !=0:
                    x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip
                    x2, y2 = lmList[8][1], lmList[8][2] # Index tip

                

                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # Center of thumb and index
            
                    cv2.circle(img, (x1, y1), 8, (255, 0, 0), cv2.FILLED)  # Draw thumb tip
                    cv2.circle(img, (x2, y2), 8, (255, 0, 0), cv2.FILLED) # Draw index tip
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3) # Draw line between thumb and index
                    cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED) # Draw center of thumb and index
                    length = math.hypot(x2 - x1, y2 - y1) # Length of line between thumb and index

                    if length < 70: 
                        cv2.circle(img, (cx, cy), 8, (0, 0,255), cv2.FILLED) 

                    currentVol = np.interp(length, [handRangeMin, handRangeMax], [minVol, maxVol])  # Interpolate volume level
                    volumeBar = np.interp(length, [handRangeMin, handRangeMax], [volumeBarMax, volumeBarMin]) # Interpolate volume bar size
                    volumePer = np.interp(length, [handRangeMin, handRangeMax], [0, 100]) # Interpolate volume percentage
                    # print(int(length), currentVol)
                    volume.SetMasterVolumeLevel(int(currentVol), None) # Seting volume
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


        # Drawing the volume box
        cv2.rectangle(img, (50, 200), (85, 350), (0 ,0, 0), 3)
        cv2.rectangle(img, (50, int(volumeBar)), (85, 350), (255,0 , 0), cv2.FILLED)
        cv2.putText(img, f'{int(volumePer)} %', (50, 390), cv2.FONT_HERSHEY_COMPLEX,1, (0, 0, 0), 3)
                

        # Calculating the fps by taking the current time and subtracting it from the previous time and dividing it by 1 to get frames in 1 second
        cTime = time.time()
        fps = 1 / (cTime - pTime) 
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,(0, 0, 255), 2) # Displaying fps on the image


        # Display the resulting frame
        cv2.imshow("Volume Controller with Hand Guesture - Pritam", img)

        # Press q to quit
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break