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

from_class = uic.loadUiType("IoT_wifi.ui")[0]
import pandas as pd
#import atexit

class CommunicationThread(QThread):
    received_signal = pyqtSignal(str)  # Signal to emit the received data
    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.running = True
        self.server_port = 9090
        self.max_users = 5 #maximum number of queued connections
        self.cmd = "5"

        self.connect()

    def connect(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(("192.168.0.23", self.server_port))
            self.server_socket.listen(self.max_users)
        except Exception as e:
            print("ERRRORRRR::: ",e)

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
                    send_data = self.cmd
                    encoded_send_data = send_data.encode('utf-8')
                    sent = client_socket.send(encoded_send_data)

                    if sent == 0:
                        print("Socket connection broken")
                    # print(sent)
                    self.received_signal.emit(decoded_data)
                # print("Disconnected")
                client_socket.close()
                count = count + 1

        except Exception as e:
            print("ERROR: ",e)
            self.server_socket.close()
            time.sleep(1)
            self.connect()

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
    update_signal = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.image_paths = ["../qr_detector/test/marker_0.png", "../qr_detector/test/marker_1.png",
                            "../qr_detector/test/marker_2.png", "../qr_detector/test/marker_3.png",
                            "../qr_detector/test/marker_4.png"]

    def run(self):
        while self.running:
            time.sleep(1)  # 1초마다 이미지 업데이트

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

        signal.signal(signal.SIGINT, self.signal_handler)

    def parsing_data(self, decoded):
        temp, humidity, co2, pm10, z_ang = 0.0, 0.0, 0, 0.0, 0.0
        split_data = decoded.split(',')
        print(split_data)
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

    def update_camera_image(self, pixmap):
        self.camera.setPixmap(pixmap)
        self.camera.setAlignment(Qt.AlignCenter)

    def cmd_1(self):
        print('hi')
        data_to_send = "1"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "1"
        
    def cmd_2(self):
        print('hi')
        data_to_send = "2"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "2"

    def cmd_3(self):
        print('hi')
        data_to_send = "3"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "3"

    def cmd_4(self):
        print('hi')
        data_to_send = "4"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "4"

    def cmd_5(self):
        print('hi')
        data_to_send = "5"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "5"
        
    def cmd_6(self):
        print('hi')
        data_to_send = "6"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "6"

    def cmd_7(self):
        print('hi')
        data_to_send = "7"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "7"

    def cmd_8(self):
        print('hi')
        data_to_send = "8"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "8"

    def cmd_9(self):
        print('hi')
        data_to_send = "9"
        # self.sensor_thread.send_serial_data(data_to_send)
        self.comm_thread.cmd = "9"

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
        for i in range(len(self.aqi_bins)):
            if aqi <= self.aqi_bins[i]:
                return self.aqi_labels[i]
        return self.aqi_labels[-1]  # 최대 범위 이상인 경우

    
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
        self.status_1.insertRow(self.row_count_1)
        self.status_1.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_1.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_1.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text())) 
        self.status_1.setItem(self.row_count_1, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_1.setItem(self.row_count_1, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "1"

        self.changeQR1Color()
        self.load_marker_image(0) 

    def Add_2(self):
        self.status_2.insertRow(self.row_count_2)
        self.status_2.setItem(self.row_count_2, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_2.setItem(self.row_count_2, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_2.setItem(self.row_count_2, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_2.setItem(self.row_count_2, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_2.setItem(self.row_count_2, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "2"

        
        self.changeQR2Color()
        self.load_marker_image(1) 

        
    def Add_3(self):
        self.status_3.insertRow(self.row_count_3)
        self.status_3.setItem(self.row_count_3, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_3.setItem(self.row_count_3, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_3.setItem(self.row_count_3, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_3.setItem(self.row_count_3, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_3.setItem(self.row_count_3, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "3"

        
        self.changeQR3Color()
        self.load_marker_image(2) 

        
    def Add_4(self):
        self.status_4.insertRow(self.row_count_4)
        self.status_4.setItem(self.row_count_4, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_4.setItem(self.row_count_4, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_4.setItem(self.row_count_4, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_4.setItem(self.row_count_4, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_4.setItem(self.row_count_4, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "4"

        self.changeQR4Color()
        self.load_marker_image(3) 

    def Add_5(self):
        self.status_5.insertRow(self.row_count_5)
        self.status_5.setItem(self.row_count_5, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_5.setItem(self.row_count_5, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_5.setItem(self.row_count_5, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_5.setItem(self.row_count_5, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_5.setItem(self.row_count_5, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "5"

        
        self.changeQR5Color()
        self.load_marker_image(4) 



        
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
    
