import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import datetime
import numpy as np
import serial
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import socket
import signal
import json

import cv2
import cv2.aruco as aruco

import math

from_class = uic.loadUiType("IoT_wifi.ui")[0]
import pandas as pd
#import atexit

class CommunicationThread(QThread):
    received_signal = pyqtSignal(str)  # Signal to emit the received data
    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.running = True
        self.server_port = 9080
        self.max_users = 5 #maximum number of queued connections
        # self.cmd = "5"
        self.cmd = ["0","5","0","0","-0","-0"]
        self.connect()

    def connect(self, ip = "192.168.0.23"):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((ip, self.server_port))
            self.server_socket.listen(self.max_users)
        except Exception as e:
            print("ERRRORRRR::: ",e)
    # [qr/manual, cmd, w1, w2, w3, w4]
    def run(self):
        count = 0
        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                # print("Connection from ", client_address)
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    decoded_data = data.decode()
                    send_data = ','.join(self.cmd).encode()
                    sent = client_socket.sendall(send_data)

                    if sent == 0:
                        print("Socket connection broken")
                    # print(sent)
                    self.received_signal.emit(decoded_data)
                # print("Disconnected")
                client_socket.close()
                count = count + 1
                QThread.msleep(10)
        except Exception as e:
            print("ERROR: ",e)
            self.server_socket.close()
            time.sleep(1)
            self.connect(ip="0.0.0.0")

    def close_socket(self):
        if hasattr(self, 'server_socket'):
            self.server_socket.close()

    def stop(self):
        self.running = False
        self.server_socket.close()
    
"""class Sensor(QThread):
    update = pyqtSignal(str)  # Signal to emit the received data

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.running = True
        self.server_address = ('your_wifi_server_ip', your_wifi_server_port)  # Replace with your actual server IP and port

    def run(self):
        time.sleep(1)
        while self.running:
            if self.py_serial.readable():
                response = self.py_serial.readline()
                try:
                    decoded_response = response.decode('utf-8').strip()
                    self.update.emit(decoded_response)  # Emit the decoded data
                except UnicodeDecodeError:
                    print("UnicodeDecodeError: Could not decode the received data.")
                    
    def stop(self):
        self.running = False
        self.py_serial.close()
    
    def send_serial_data(self, data):
        # Send data to the serial port
        encoded_data = data.encode('utf-8')
        self.py_serial.write(encoded_data)"""

class ImageLoaderThread(QThread):
    update_signal = pyqtSignal(QPixmap, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.image_paths = ["../qr_detector/test/marker_0.png", "../qr_detector/test/marker_1.png",
                            "../qr_detector/test/marker_2.png", "../qr_detector/test/marker_3.png",
                            "../qr_detector/test/marker_4.png"]
        self.qr_info = []
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0

    def init_cam(self):
        global blue_BGR, marker_3d_edges, cmtx, dist

        self.cap = self.use_esp_cam()
        cmtx = [[376.0221020,0.0,176.19498204],
            [0.0,386.25988369,124.674899],
            [0.0,0.0,1.0],]
        dist = [-6.83045077e-02,  1.64416917e+00, -3.89914235e-03,  1.29325474e-02,  -6.00400981e+00]
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        blue_BGR = (255, 0, 0)
        marker_size = 200 # pixel
        marker_3d_edges = np.array([    [0,0,0],
                                        [0,marker_size,0],
                                        [marker_size,marker_size,0],
                                        [marker_size,0,0]], dtype = 'float32').reshape((4,1,3))


    def run(self):
        global blue_BGR, marker_3d_edges, cmtx, dist
        self.cap = self.use_esp_cam()
        cmtx = [[376.0221020,0.0,176.19498204],
            [0.0,386.25988369,124.674899],
            [0.0,0.0,1.0],]
        dist = [-6.83045077e-02,  1.64416917e+00, -3.89914235e-03,  1.29325474e-02,  -6.00400981e+00]
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        blue_BGR = (255, 0, 0)
        marker_size = 200 # pixel
        marker_3d_edges = np.array([    [0,0,0],
                                        [0,marker_size,0],
                                        [marker_size,marker_size,0],
                                        [marker_size,0,0]], dtype = 'float32').reshape((4,1,3))

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
                frame_cen = frame.copy()

                frame_cen, qr_info = self.find_center_pt(ids, frame_cen, corners)

                pixmap = self.cv2_to_qpixmap(frame_cen)
                self.update_signal.emit(pixmap, qr_info)
                QThread.msleep(10)

    def cv2_to_qpixmap(self, cv_img):
        height, width, channel = cv_img.shape
        bytesPerLine = 3 * width
        qImg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(qImg)


    def load_image(self, path):
        try:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                return pixmap
        except Exception as e:
            print(f"Error loading image: {e}")
        return None

    def stop(self):
        self.running = False
        self.quit()


    def find_center_pt(self, ids, frame, corners):
        global blue_BGR, marker_3d_edges, cmtx, dist
        self.qr_info.clear()
        for i in range(len(corners)):
            corner = corners[i][0]
            ret, rvec, tvec = cv2.solvePnP(marker_3d_edges, corner, np.array(cmtx), np.array(dist))
            center_x = int((corner[:, 0].min() + corner[:, 0].max()) / 2)
            center_y = int((corner[:, 1].min() + corner[:, 1].max()) / 2)
            id = ids[i][0]
            cen_point = f"{center_x}, {center_y}"

            # Get rpy (roll, pitch, yaw)
            rpy = np.degrees(cv2.Rodrigues(rvec)[0].T[0])

            cv2.putText(frame, f"ID={id}",(int(center_x), int(center_y)), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 0, 255))
            cv2.putText(frame, cen_point,(int(center_x)-20, int(center_y)+20), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 0, 255))
            cv2.circle(frame, (center_x, center_y), 4, (0, 255, 0), -1)

            cv2.putText(frame, f"{rpy[0]:.2f}, {rpy[1]:.2f}, {rpy[2]:.2f}", (int(center_x)-70, int(center_y) + 40),
                    cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 0, 255))
            
            # Draw xyz coordinates
            axis_points, _ = cv2.projectPoints(marker_3d_edges, rvec, tvec, np.array(cmtx), np.array(dist))
            axis_points = np.int32(axis_points).reshape(-1, 2)
            cv2.drawContours(frame, [axis_points[:4]], -1, (0, 255, 0), 3)
            
            self.x = center_x
            self.y = center_y
            self.yaw = rpy[0]
            data = [id, self.x, self.y, self.yaw]
            self.qr_info.append(data)
        return frame, self.qr_info

    def use_esp_cam(self):
        # SERVER_IP = '192.168.0.37'
        SERVER_IP = '192.168.0.2'
        PORT = 81
        esp_url = f"http://{SERVER_IP}:{PORT}/stream"
        cap = cv2.VideoCapture(esp_url)
        return cap


class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.isSensorOn = False
        self.place = "0"
        # 첫 번째 컬럼 크기 설정
        self.LiveStatus.horizontalHeader().resizeSection(0, 150)
        self.LiveStatus.horizontalHeader().resizeSection(5, 30)

        # 나머지 컬럼은 Stretch 모드로 자동 조절
        for i in range(1, self.LiveStatus.horizontalHeader().count()-1):
            self.LiveStatus.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            
        self.status_1.horizontalHeader().resizeSection(0, 150)
        for i in range(1, self.status_1.horizontalHeader().count()):
            self.status_1.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            
        self.status_2.horizontalHeader().resizeSection(0, 150)
        for i in range(1, self.status_2.horizontalHeader().count()):
            self.status_2.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            
        self.status_3.horizontalHeader().resizeSection(0, 150)
        for i in range(1, self.status_3.horizontalHeader().count()):
            self.status_3.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            
        self.status_4.horizontalHeader().resizeSection(0, 150)
        for i in range(1, self.status_4.horizontalHeader().count()):
            self.status_4.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            
        self.status_5.horizontalHeader().resizeSection(0, 150)
        for i in range(1, self.status_5.horizontalHeader().count()):
            self.status_5.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            
        self.color = QColor(255, 0, 0)
        self.white = QColor(255, 255, 255)
        
        self.test.clicked.connect(self.Add_1)
        self.test_2.clicked.connect(self.Add_2)
        self.test_3.clicked.connect(self.Add_3)
        self.test_4.clicked.connect(self.Add_4)
        self.test_5.clicked.connect(self.Add_5)
        self.btnExport.clicked.connect(self.exportTable)
        self.btnReset.clicked.connect(self.reset)
        
        self.btncmd_1.clicked.connect(self.cmd_7)
        self.btncmd_2.clicked.connect(self.cmd_8)
        self.btncmd_3.clicked.connect(self.cmd_9)
        self.btncmd_4.clicked.connect(self.cmd_4)
        self.btncmd_5.clicked.connect(self.cmd_5)
        self.btncmd_6.clicked.connect(self.cmd_6)
        self.btncmd_7.clicked.connect(self.cmd_1)
        self.btncmd_8.clicked.connect(self.cmd_2)
        self.btncmd_9.clicked.connect(self.cmd_3)
        self.btncmd_emer.clicked.connect(self.cmd_emer)


        self.qr_move = False
        self.manual_move = False
        self.qr_btn.clicked.connect(self.qr_mode)
        self.manual_btn.clicked.connect(self.manual_mode)
        self.manual_L.clicked.connect(self.manual_L_move)
        self.manual_R.clicked.connect(self.manual_R_move)
        
                
        self.row_count_1 = self.status_1.rowCount()
        self.row_count_2 = self.status_2.rowCount()
        self.row_count_3 = self.status_3.rowCount()
        self.row_count_4 = self.status_4.rowCount()
        self.row_count_5 = self.status_5.rowCount()
        self.LiveStatus.insertRow(0)

        # self.sensor_thread = Sensor(self)
        # self.sensor_thread.update.connect(self.handle_sensor_data)

        self.cols = ['Date', 'Temperature (°C)', 'Humidity (%)', 'Co2 (ppm)', 'PM-10 (μg/m3)', 'Place']
       
        self.btnplot.clicked.connect(self.popPlot) 
        
        self.timestamps = []
        self.temperatures = []
        self.humidities = []
        self.co2_levels = []
        self.pm10_levels = []
        self.show_danger = False
        self.last_danger_time = None
        
        self.aqi_bins = [0, 50, 100, 250, 500]
        self.aqi_labels = ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy']
        self.data = []

        self.comm_thread = CommunicationThread()
        self.comm_thread.received_signal.connect(self.parsing_data)
        self.comm_thread.start()
        self.comm_thread.running = True
        # self.comm_thread.update.connect(self.handle_sensor_data)
        self.z_val = 0
        
        self.image_loader_thread = ImageLoaderThread(self)
        self.image_loader_thread.update_signal.connect(self.update_camera_image)
        self.image_loader_thread.start()
        self.qr_info = []
        self.temp_id = None
        self.yaw_flag = False
        self.x_flag = False
        self.y_flag = False
        self.corr_done = False
        self.cur_pos = [0, 0]

        signal.signal(signal.SIGINT, self.signal_handler)

    def qr_mode(self):
        self.qr_move = True
        self.manual_move = False
        self.corr_done = False
        self.yaw_flag = False
        self.x_flag = False
        self.y_flag = False
        self.temp_id = None

    def manual_mode(self):
        self.manual_move = True
        self.qr_move = False

    def manual_L_move(self):
        self.comm_thread.cmd = ["0","60","0","0","0","0"]

    
    def manual_R_move(self):
        self.comm_thread.cmd = ["0","66","0","0","0","0"]


    def parsing_data(self, decoded):
        temp, humidity, co2, pm10, z_ang = 0.0, 0.0, 0, 0.0, 0.0
        split_data = decoded.split(',')
        # print(split_data)
        try:
            temp = 0.0
            humidity = 0.0
            co2 = int(split_data[0].strip()) # sv
            pm10 = float(split_data[1].strip()) # dust
            z_ang = int(split_data[2].strip()) # imu
        except :
            print("parsing_data : Sensor Error")
            
        self.data = [temp, humidity, co2, pm10, z_ang]
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # if len(self.data) < 5:
        #     pass
        # else:
        #     temp, humidity, co2, pm10,  z_ang= 0.0, 0.0, 0, 0.0, 0

        self.LiveStatus.setItem(0, 0, QTableWidgetItem(current_time))
        self.LiveStatus.setItem(0, 1, QTableWidgetItem(str(temp)))
        self.LiveStatus.setItem(0, 2, QTableWidgetItem(str(humidity)))
        self.LiveStatus.setItem(0, 3, QTableWidgetItem(str(co2)))
        self.LiveStatus.setItem(0, 4, QTableWidgetItem(str(pm10)))
        self.LiveStatus.setItem(0, 5, QTableWidgetItem(self.place))
        self.label_z.setText("Z : {}".format(z_ang))

        aqi = self.calculate_aqi(pm10)
        status = self.get_aqi_status(aqi)
        self.feedback.setText(status)

    def signal_handler(self, sig, frame):
        self.comm_thread.close_socket()

    def cmd_emer(self) :
        # self.sensor_thread.running = False
        # self.sensor_thread.stop()
        print("hi")

    def load_marker_image(self, marker_index):
        if 0 <= marker_index < len(self.image_loader_thread.image_paths):
            image_path = self.image_loader_thread.image_paths[marker_index]
            pixmap = self.image_loader_thread.load_image(image_path)
            if pixmap:
                self.image_loader_thread.update_signal.emit(pixmap)

    def update_camera_image(self, pixmap, qr_info):
        self.camera.setPixmap(pixmap)
        self.camera.setAlignment(Qt.AlignCenter)
        # print(qr_info)
        try:
            self.qr_info = qr_info
            id = self.qr_info[0][0]
            if id != self.temp_id:
                self.corr_done = False

            if self.qr_move and not self.corr_done:
                self.cal_qr_cmd()
        except:
            pass
    def move(self, distance, direction):
        self.cur_pos[0] += distance * np.cos(direction)
        self.cur_pos[1] += distance * np.sin(direction)

    def cal_qr_cmd(self):
        try:
            # print(self.qr_info[0])
            id = self.qr_info[0][0]
            x = self.qr_info[0][1]
            y = self.qr_info[0][2]
            yaw = self.qr_info[0][3]
            width = 320
            height = 240

            target_x = width/2.0
            target_y = height/2.0

            if self.temp_id != id:
                self.temp_id = id
                self.yaw_flag = False
                self.x_flag = False
                self.y_flag = False


            now_x_diff = width - x
            now_y_diff = height - y
            cal_x = x - now_x_diff
            cal_y = y - now_y_diff


            arc_x, arc_y = x, y
            delta_x = target_x - arc_x
            delta_y = target_y - arc_y

            distance = np.sqrt(delta_x**2 + delta_y**2)
            angle = np.arctan2(delta_x, delta_y)

            vx = distance * np.cos(angle) * 0.08
            vz = angle * 0.5

            # print(vx, vz)

            r = 0.025
            b = 0.11
            w1 = (1/r) * (vx-vz*b/2)
            w2 = (1/r) * (vx+vz*b/2)
            w3 = (1/r) * (vx-vz*b/2)
            w4 = (1/r) * (vx+vz*b/2)

            if abs(w1)>120:
                if w1>0:
                    w1 = 120
                else:
                    w1 = -120
            if abs(w2)>120:
                if w2>0:
                    w2 = 120
                else:
                    w2 = -120
            if abs(w3)>120:
                if w3>0:
                    w3 = 120
                else :
                    w3 = -120
            if abs(w4)>120:
                if w4>0:
                    w4 = 120
                else:
                    w4 = -120
            # print(w1, w2, w3, w4)
            self.comm_thread.cmd = ["1","5",str(w4),str(w1),str(w2),str(w3)]

        except Exception as e:
            # print(e)
            pass

    def cmd_1(self):
        print('hi')
        data_to_send = "1"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","1","0","0","0","0"]

    def cmd_2(self):
        print('hi')
        data_to_send = "2"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","2","0","0","0","0"]

    def cmd_3(self):
        print('hi')
        data_to_send = "3"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","3","0","0","0","0"]


    def cmd_4(self):
        print('hi')
        data_to_send = "4"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","4","0","0","0","0"]


    def cmd_5(self):
        print('hi')
        data_to_send = "5"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","5","0","0","0","0"]

        
    def cmd_6(self):
        print('hi')
        data_to_send = "6"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","6","0","0","0","0"]


    def cmd_7(self):
        print('hi')
        data_to_send = "7"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","7","0","0","0","0"]


    def cmd_8(self):
        print('hi')
        data_to_send = "8"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","8","0","0","0","0"]


    def cmd_9(self):
        print('hi')
        data_to_send = "9"
        # self.sensor_thread.send_serial_data(data_to_send)
        if self.manual_move:
            self.comm_thread.cmd = ["0","9","0","0","0","0"]

    def update_data(self, frame):
        # 데이터를 파싱하여 각 변수에 저장
        if len(self.data) >= 4:
            temp = self.data[0]
            humidity = self.data[1]
            co2 = self.data[2]
            pm10 = self.data[3]
            # temp = float(self.data[0].split(":")[1].strip().replace("°C", ""))
            # humidity = float(self.data[1].split(":")[1].strip().replace("%", ""))
            # co2 = int(self.data[2].split(":")[1].strip().replace("ppm", ""))
            # pm10 = float(self.data[3].split(":")[1].strip().replace("ug/m3", ""))
        else:
        # 기본값 할당
            temp, humidity, co2, pm10 = 0.0, 0.0, 0, 0.0
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        # 데이터를 리스트에 추가
        self.timestamps.append(timestamp)
        self.temperatures.append(temp)
        self.humidities.append(humidity)
        self.co2_levels.append(co2)
        self.pm10_levels.append(pm10)

        # Danger 메시지 표시 관리
        if pm10 >= 100:
            self.show_danger = True
            last_danger_time = time.time()
        elif self.show_danger and time.time() - last_danger_time > 3:
            self.show_danger = False

        # AQI 계산
        aqi = self.calculate_aqi(pm10)
        status = self.get_aqi_status(aqi)

        # 그래프 업데이트
        self.ax.clear()
        self.ax.plot(self.timestamps, self.temperatures, label='Temperature (°C)')
        self.ax.plot(self.timestamps, self.humidities, label='Humidity (%)')
        self.ax.plot(self.timestamps, self.co2_levels, label='CO2 (ppm)')
        self.ax.plot(self.timestamps, self.pm10_levels, label='PM10 (ug/m3)')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.set_title(f'Sensor Data Over Time - AQI: {aqi}, Status: {status}')
        self.ax.legend()
        self.ax.grid(True)
        self.ax.tick_params(axis='x', rotation=45)
        
        # Danger 메시지 표시
        if self.show_danger:
            self.ax.text(0.5, 0.5, "Danger!!!", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, fontsize=20, color='red')
        self.ax.figure.canvas.draw()

    # AQI 계산 함수
    def calculate_aqi(self, pm10):
        return ((100 - 51) / (80 - 31)) * (pm10 - 31) + 51

    # AQI 상태 가져오기 함수
    def get_aqi_status(self, aqi):
        try:
            for i in range(len(self.aqi_bins)):
                if aqi <= self.aqi_bins[i]:
                    return self.aqi_labels[i]
            return self.aqi_labels[-1]  # 최대 범위 이상인 경우
        except Exception as e:
            print("get_aqi_status : ", e)

    
    def popPlot(self) :
        # 그래프 생성
        fig, self.ax = plt.subplots(figsize=(10, 6))

        # 애니메이션 생성
        self.ani = FuncAnimation(fig, self.update_data, interval=1000)

        # 그래프 표시
        plt.show()


    def exportTable(self):
        table_1 = pd.DataFrame(self.getTable(self.status_1,1), columns=self.cols).to_csv('~/amr_ws/IoT/data/table/table_1.csv', index=False)
        table_2 = pd.DataFrame(self.getTable(self.status_2,2), columns=self.cols).to_csv('~/amr_ws/IoT/data/table/table_2.csv', index=False)
        table_3 = pd.DataFrame(self.getTable(self.status_3,3), columns=self.cols).to_csv('~/amr_ws/IoT/data/table/table_3.csv', index=False)
        table_4 = pd.DataFrame(self.getTable(self.status_4,4), columns=self.cols).to_csv('~/amr_ws/IoT/data/table/table_4.csv', index=False)
        table_5 = pd.DataFrame(self.getTable(self.status_5,5), columns=self.cols).to_csv('~/amr_ws/IoT/data/table/table_5.csv', index=False)


    def reset(self) :
 
        self.status_1.setRowCount(0)
        self.status_2.setRowCount(0)
        self.status_3.setRowCount(0)
        self.status_4.setRowCount(0)
        self.status_5.setRowCount(0)

    """def clickSensor(self):
        if self.isSensorOn == False:
            self.btnSensor.setText("Sensor off")
            self.isSensorOn = True
            self.SensorStart()
        else :
            self.btnSensor.setText('Sensor on')
            
            self.isSensorOn = False
            self.SensorStop()

    def SensorStart(self):
        self.sensor_thread.running = True
        self.sensor_thread.start()

    def SensorStop(self):
        self.sensor_thread.running = False
        
        try:
            #atexit.register(self.sensor_thread.py_serial.close())
            self.sensor_thread.py_serial.close()
        except Exception as e:
            print(e)"""
    
        
    def handle_sensor_data(self, line):       
        temp, humidity, co2, pm10, z_ang = 0.0, 0.0, 0, 0.0, 0.0
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        if not line.startswith("Temperature:"):
            return
        self.data = line.split(",")
        """temp = float(data[0].split(":")[1].strip().replace("°C", ""))
        humidity = float(data[1].split(":")[1].strip().replace("%", ""))
        co2 = int(data[2].split(":")[1].strip().replace("ppm", ""))
        pm10 = float(data[3].split(":")[1].strip().replace("ug/m3", ""))"""
        
        if len(self.data) >= 5:
            # Temperature
            try :
                temp = float(self.data[0].split(":")[1].strip().replace("°C", ""))
                
                # Humidity
                humidity = float(self.data[1].split(":")[1].strip().replace("%", ""))
                
                # CO2
                co2 = int(self.data[2].split(":")[1].strip().replace("ppm", ""))
                
                # PM10
                pm10 = float(self.data[3].split(":")[1].strip().replace("ug/m3", ""))
                
                # z_ang = float(self.data[4])
                z_ang = self.z_val
            except :
                print("Sensor Error")
        else:
        # 기본값 할당
            temp, humidity, co2, pm10,  z_ang= 0.0, 0.0, 0, 0.0, 0

        self.LiveStatus.setItem(0, 0, QTableWidgetItem(current_time))
        self.LiveStatus.setItem(0, 1, QTableWidgetItem(str(temp)))
        self.LiveStatus.setItem(0, 2, QTableWidgetItem(str(humidity)))
        self.LiveStatus.setItem(0, 3, QTableWidgetItem(str(co2)))
        self.LiveStatus.setItem(0, 4, QTableWidgetItem(str(pm10)))
        self.LiveStatus.setItem(0, 5, QTableWidgetItem(self.place))
        self.label_z.setText("Z : {}".format(z_ang))

        aqi = self.calculate_aqi(pm10)
        status = self.get_aqi_status(aqi)
        
        self.feedback.setText(status)
        
        
    def Add_1(self):
        # self.status_1.insertRow(self.row_count_1)
        # self.status_1.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        # self.status_1.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        # self.status_1.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text())) 
        # self.status_1.setItem(self.row_count_1, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        # self.status_1.setItem(self.row_count_1, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        # self.place = "1"

        # self.changeQR1Color()
        # self.load_marker_image(0) 
        self.comm_thread.cmd = ["1","5","100","0","0","0"]

    def Add_2(self):
        # self.status_2.insertRow(self.row_count_2)
        # self.status_2.setItem(self.row_count_2, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        # self.status_2.setItem(self.row_count_2, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        # self.status_2.setItem(self.row_count_2, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        # self.status_2.setItem(self.row_count_2, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        # self.status_2.setItem(self.row_count_2, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        # self.place = "2"

        
        # self.changeQR2Color()
        # self.load_marker_image(1) 
        self.comm_thread.cmd = ["1","5","0","100","0","0"]


        
    def Add_3(self):
        # self.status_3.insertRow(self.row_count_3)
        # self.status_3.setItem(self.row_count_3, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        # self.status_3.setItem(self.row_count_3, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        # self.status_3.setItem(self.row_count_3, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        # self.status_3.setItem(self.row_count_3, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        # self.status_3.setItem(self.row_count_3, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        # self.place = "3"

        
        # self.changeQR3Color()
        # self.load_marker_image(2) 
        self.comm_thread.cmd = ["1","5","0","0","100","0"]

        
    def Add_4(self):
        # self.status_4.insertRow(self.row_count_4)
        # self.status_4.setItem(self.row_count_4, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        # self.status_4.setItem(self.row_count_4, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        # self.status_4.setItem(self.row_count_4, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        # self.status_4.setItem(self.row_count_4, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        # self.status_4.setItem(self.row_count_4, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        # self.place = "4"

        # self.changeQR4Color()
        # self.load_marker_image(3) 
        self.comm_thread.cmd = ["1","5","0","0","0","100"]


    def Add_5(self):
        # self.status_5.insertRow(self.row_count_5)
        # self.status_5.setItem(self.row_count_5, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        # self.status_5.setItem(self.row_count_5, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        # self.status_5.setItem(self.row_count_5, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        # self.status_5.setItem(self.row_count_5, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        # self.status_5.setItem(self.row_count_5, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        # self.place = "5"

        
        # self.changeQR5Color()
        # self.load_marker_image(4) 
        self.comm_thread.cmd = ["1","5","0","0","0","0"]



        
    def changeQR1Color(self):
        self.QR_1.setStyleSheet("background-color: {}".format(self.color.name()))
        self.QR_2.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_3.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_4.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_5.setStyleSheet("background-color: {}".format(self.white.name()))
        
    def changeQR2Color(self):
        self.QR_1.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_2.setStyleSheet("background-color: {}".format(self.color.name()))
        self.QR_3.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_4.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_5.setStyleSheet("background-color: {}".format(self.white.name()))
                
    def changeQR3Color(self):
        self.QR_1.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_2.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_3.setStyleSheet("background-color: {}".format(self.color.name()))
        self.QR_4.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_5.setStyleSheet("background-color: {}".format(self.white.name()))
        
    def changeQR4Color(self):
        self.QR_1.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_2.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_3.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_4.setStyleSheet("background-color: {}".format(self.color.name()))
        self.QR_5.setStyleSheet("background-color: {}".format(self.white.name()))
        
    def changeQR5Color(self):
        self.QR_1.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_2.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_3.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_4.setStyleSheet("background-color: {}".format(self.white.name()))
        self.QR_5.setStyleSheet("background-color: {}".format(self.color.name()))
        

    def getTable(self, table, btn_num):
        table_list = []
        for i in range(table.rowCount()):
            row_data = []
            for j in range(table.columnCount()):
                item = table.item(i, j)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # If cell is empty, add an empty string
            row_data.append(btn_num)
            table_list.append(row_data)
        return table_list



        
        
        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())
    
