import cv2
import cv2.aruco as aruco
import time 
import numpy as np 

def main():
    # 카메라 캡처
    cap = cv2.VideoCapture(0)
    width = 640
    height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # camera matrix
    cmtx = [[430.215550,0.0,306.691343],
            [0.0,430.531693,227.224800],
            [0.0,0.0,1.0],]
    # distortion
    dist = [-0.337586, 0.111612, -0.000218, -0.000030, 0.0000]
    print(dist)

    # Aruco 디텍터 설정
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    # time.sleep(2)

    blue_BGR = (255, 0, 0)

    # marker_size = 35
    marker_size = 400 # pixel
    marker_3d_edges = np.array([    [0,0,0],
                                    [0,marker_size,0],
                                    [marker_size,marker_size,0],
                                    [marker_size,0,0]], dtype = 'float32').reshape((4,1,3))

    while True:
        ret, frame = cap.read()
        if ret:
            # 흑백으로 변환
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Aruco 마커 검출
            corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
            if ids is not None:
                # 마커가 검출되었을 경우, 검출된 마커에 draw
                # frame = aruco.drawDetectedMarkers(frame, corners, ids) 
                pass

            # print(len(corners))
            for corner in corners:
                corner = np.array(corner).reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corner

                topRightPoint    = (int(topRight[0]),      int(topRight[1]))
                topLeftPoint     = (int(topLeft[0]),       int(topLeft[1]))
                bottomRightPoint = (int(bottomRight[0]),   int(bottomRight[1]))
                bottomLeftPoint  = (int(bottomLeft[0]),    int(bottomLeft[1]))

                cv2.circle(frame, topLeftPoint, 4, blue_BGR, -1)
                cv2.circle(frame, topRightPoint, 4, blue_BGR, -1)
                cv2.circle(frame, bottomRightPoint, 4, blue_BGR, -1)
                cv2.circle(frame, bottomLeftPoint, 4, blue_BGR, -1)

                # PnP
                ret, rvec, tvec = cv2.solvePnP(marker_3d_edges, corner, np.array(cmtx), np.array(dist))
                if(ret):
                    x=round(tvec[0][0],2)
                    y=round(tvec[1][0],2)
                    z=round(tvec[2][0],2)
                    rx=round(np.rad2deg(rvec[0][0]),2)
                    ry=round(np.rad2deg(rvec[1][0]),2)
                    rz=round(np.rad2deg(rvec[2][0]),2)
                    # PnP result put text
                    text1 = f"{x},{y},{z}"
                    text2 = f"{rx},{ry},{rz}"
                    cv2.putText(frame, text1, (int(topLeft[0]-10),   int(topLeft[1]+10)), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))
                    cv2.putText(frame, text2, (int(topLeft[0]-10),   int(topLeft[1]+40)), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))

            # 화면에 표시
            cv2.imshow('frame', frame)

            # 'q' 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # 종료
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


# image = cv2.imread("marker_0.png")
# # cvt_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# corners, ids, rejectedImgPoints = detector.detectMarkers(image)
# print(corners,ids,rejectedImgPoints)
# # if ids is not None:
# image = aruco.drawDetectedMarkers(image, corners, ids) 

# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()