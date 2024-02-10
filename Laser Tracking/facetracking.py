import cv2, numpy as np, time, serial, subprocess
from cvzone.FaceDetectionModule import FaceDetector

compile_process = subprocess.Popen(["arduino-cli", "compile", "--fqdn", "arduino:avr:uno", "Firmata"])
upload_process = subprocess.Popen(["arduino-cli", "upload", "-p", "COM11", "--fqdn", "arduino:avr:uno", "Firmata"])

compile_process.wait()
upload_process.wait()
time.sleep(2)

ser = serial.Serial('COM11', 9600)

cap = cv2.VideoCapture(0)
ws, hs = 1280, 7201
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Seems like there's a problem....")
    exit()

detector = FaceDetector()
servoPos = [90, 90]

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
        pos = [fx, fy]

        servoX = np.interp(fx, [0, ws], [0, 180])
        servoY = np.interp(fy, [0, hs], [0, 180])
        servoX = max(0, min(180, servoX))
        servoY = max(0, min(180, servoY))
        servoPos[0] = servoX
        servoPos[1] = servoY

        cv2.putText(img, "TARGET LOCKED", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.rectangle(img, (fx-150, fy-200), (fx+150, fy+200), (173, 216, 230), 2)


    else:
        cv2.putText(img, "NO TARGET", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    ser.write(f"{int(servoPos[0])},{int(servoPos[1])}\n".encode())
    cv2.imshow("image", img)
    cv2.waitKey(1)