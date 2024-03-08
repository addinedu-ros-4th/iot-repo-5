import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt

# 마커 사이즈 설정
marker_size = 200

# Aruco 딕셔너리 생성
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# 마커 생성 및 표출
# fig = plt.figure()
# for i in range(5):  # 5개의 마커 생성
#     marker_id = i
#     marker_image = aruco.drawMarker(aruco_dict, marker_id, marker_size)
    
#     # matplotlib를 사용하여 마커 이미지 출력
#     ax = fig.add_subplot(1, 5, i+1)
#     ax.imshow(marker_image, cmap='gray')
#     ax.axis('off')
#     ax.set_title(f'Marker {marker_id}')

# plt.show()

# 마커 생성 및 저장
for i in range(5):  # 5개의 마커 생성
    marker_id = i
    marker_image = aruco.drawMarker(aruco_dict, marker_id, marker_size)
    
    # 이미지 파일로 저장
    cv2.imwrite(f"marker_{marker_id}.png", marker_image)