import cv2
import cv2.aruco as aruco

# 카메라 캡처
cap = cv2.VideoCapture(0)
width = 1024
height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# 새로운 해상도 확인
new_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
new_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print("New camera resolution:", new_width, "x", new_height)
# Aruco 디텍터 설정
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

# image = cv2.imread("marker_0.png")
# # cvt_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# corners, ids, rejectedImgPoints = detector.detectMarkers(image)
# print(corners,ids,rejectedImgPoints)
# # if ids is not None:
# image = aruco.drawDetectedMarkers(image, corners, ids) 

# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

while True:
    ret, frame = cap.read()
    if ret:
        # 흑백으로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aruco 마커 검출
        # corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
        if ids is not None:
            # 마커가 검출되었을 경우, 검출된 마커를 표시
            frame = aruco.drawDetectedMarkers(frame, corners, ids) 

        # 화면에 표시
        cv2.imshow('frame', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 종료
cap.release()
cv2.destroyAllWindows()