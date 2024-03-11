import cv2
import numpy as np
import socket

SERVER_IP = '192.168.101.6'
PORT = 81
esp_url = f"http://{SERVER_IP}:{PORT}/stream"
cap = cv2.VideoCapture(esp_url)

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Failed to receive frame")
            continue

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()
