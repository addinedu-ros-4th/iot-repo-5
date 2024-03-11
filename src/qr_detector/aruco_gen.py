import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt


if __name__ == "__main__":
    board_type = aruco.DICT_6X6_250
    marker_size = 200 
    aruco_dict = aruco.getPredefinedDictionary(board_type)

    # fig = plt.figure()
    # for i in range(5):  
    #     marker_id = i
    #     marker_image = aruco.drawMarker(aruco_dict, marker_id, marker_size)
    #     ax = fig.add_subplot(1, 5, i+1)
    #     ax.imshow(marker_image, cmap='gray')
    #     ax.axis('off')
    #     ax.set_title(f'Marker {marker_id}')

    # plt.show()

    # 마커 생성 및 저장
    for i in range(10): 
        marker_id = i
        marker_image = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
        
        cv2.imwrite(f"marker_{marker_id}.png", marker_image)