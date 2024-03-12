import cv2
import cv2.aruco as aruco
import numpy as np

import time 
import socket

def find_center_pt(frame, corners):
    global blue_BGR, marker_3d_edges, cmtx, dist

    for i in range(len(corners)):
        corner = corners[i][0]
        center_x = int((corner[:, 0].min() + corner[:, 0].max()) / 2)
        center_y = int((corner[:, 1].min() + corner[:, 1].max()) / 2)
        cen_point = f"{center_x}, {center_y}"

        cv2.putText(frame, cen_point,(int(center_x + 10), int(center_y + 10)), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))
        cv2.circle(frame, (center_x, center_y), 4, (0, 255, 0), -1)

    return frame

def find_corner_pnp(frame, corners):
    global blue_BGR, marker_3d_edges, cmtx, dist

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

    return frame


def use_usb_cam():
    # 카메라 캡처
    cap = cv2.VideoCapture(0)

    return cap

def use_esp_cam():
    SERVER_IP = '192.168.0.37'
    PORT = 81
    esp_url = f"http://{SERVER_IP}:{PORT}/stream"
    cap = cv2.VideoCapture(esp_url)
    return cap

def main():
    global blue_BGR, marker_3d_edges, cmtx, dist

    cap = use_esp_cam()
    width = 640
    height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # camera matrix
    # cmtx = [[430.215550,0.0,306.691343],
    #         [0.0,430.531693,227.224800],
    #         [0.0,0.0,1.0],]

    cmtx = [[376.0221020,0.0,176.19498204],
            [0.0,386.25988369,124.674899],
            [0.0,0.0,1.0],]

    # distortion
    # dist = [-0.337586, 0.111612, -0.000218, -0.000030, 0.0000]
    dist = [-6.83045077e-02,  1.64416917e+00, -3.89914235e-03,  1.29325474e-02,  -6.00400981e+00]
    # print(dist)

    # Aruco 디텍터 설정
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    blue_BGR = (255, 0, 0)

    # marker_size = 35
    marker_size = 200 # pixel
    marker_3d_edges = np.array([    [0,0,0],
                                    [0,marker_size,0],
                                    [marker_size,marker_size,0],
                                    [marker_size,0,0]], dtype = 'float32').reshape((4,1,3))
    
    while True:
        ret, frame = cap.read()
        if ret:
            # Aruco 마커 검출
            # frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

            if ids is not None:
                # 마커가 검출되었을 경우, 검출된 마커에 draw
                # frame = aruco.drawDetectedMarkers(frame, corners, ids) 
                pass

            frame_cen = frame.copy()
            # frame_pnp = frame.copy()

            frame_cen = find_center_pt(frame_cen, corners)
            # frame_pnp = find_corner_pnp(frame_pnp, corners)

            # 화면에 표시
            # cv2.imshow('gray', gray)
            # cv2.imshow('frame_pnp', frame_pnp)
            cv2.imshow('frame_cen', frame_cen)

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