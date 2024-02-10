import mediapipe, cv2, time, serial, subprocess, numpy as np

compile_process = subprocess.Popen(["arduino-cli", "compile", "--fqdn", "arduino:avr:uno", "Firmata"])
upload_process = subprocess.Popen(["arduino-cli", "upload", "-p", "COM11", "--fqdn", "arduino:avr:uno", "Firmata"])

compile_process.wait()
upload_process.wait()
time.sleep(2)

ser = serial.Serial('COM11', 2000000)

drawModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

cap = cv2.VideoCapture(0)
servoPos = [90, 90]
ws, hs = 1280, 720
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
    
    while True:
        ret, frame = cap.read()
        frame1 = cv2.resize(frame, (ws, hs))
        results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks != None:
            
            for handLandmarks in results.multi_hand_landmarks:
                drawModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                
                for point in handsModule.HandLandmark:
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = drawModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 640, 480)
                    
                    if point == 8:
                        print(point)
                        print(normalizedLandmark)
                        servoPos[0] = pixelCoordinatesLandmark[0]
                        servoPos[1] = pixelCoordinatesLandmark[1]
                        print(servoPos[0])
                        print(servoPos[1])
        
        ser.write(f"{int(servoPos[0])}, {int(servoPos[1])}\n".encode())
        cv2.imshow("frame", frame1);
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
