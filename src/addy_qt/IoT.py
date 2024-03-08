import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import datetime
import numpy as np
import serial


from_class = uic.loadUiType("IoT.ui")[0]
import pandas as pd

class Sensor(QThread):
    update = pyqtSignal(str)  # Signal to emit the received data

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.running = True
        self.py_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

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

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.isSensorOn = False

        self.LiveStatus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.status_1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.status_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.status_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.status_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.status_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.color = QColor(255, 0, 0)
        self.white = QColor(255, 255, 255)
        
        self.test.clicked.connect(self.Add_1)
        self.test_2.clicked.connect(self.Add_2)
        self.test_3.clicked.connect(self.Add_3)
        self.test_4.clicked.connect(self.Add_4)
        self.test_5.clicked.connect(self.Add_5)
        self.btnSensor.clicked.connect(self.clickSensor)
        
        self.row_count_1 = self.status_1.rowCount()
        self.row_count_2 = self.status_2.rowCount()
        self.row_count_3 = self.status_3.rowCount()
        self.row_count_4 = self.status_4.rowCount()
        self.row_count_5 = self.status_5.rowCount()
        self.LiveStatus.insertRow(0)
        self.status_1.insertRow(0)
        self.status_2.insertRow(0)
        self.status_3.insertRow(0)
        self.status_4.insertRow(0)
        self.status_5.insertRow(0)


        self.sensor_thread = Sensor(self)
        self.sensor_thread.update.connect(self.handle_sensor_data)

    def clickSensor(self):
        if self.isSensorOn == False:
            self.btnSensor.setText("Sensor off")
            self.isSensorOn = True
            self.SensorStart()
        else :
            self.btnSensor.setText('Sensor on')
            self.isSensorOn = False
            self.SensorStop()

    def SensorStart(self):
        self.camera.running = True
        self.sensor_thread.start()

    def SensorStop(self):
        self.sensor_thread.running = False
        self.py_serial.close()
        
    def handle_sensor_data(self, data):
        # Process the received sensor data here
        data_sp = data.split()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

        if len(data_sp) >= 2:
            self.LiveStatus.setItem(0, 0, QTableWidgetItem(data_sp[0]))
            self.LiveStatus.setItem(0, 1, QTableWidgetItem(data_sp[1]))
            self.LiveStatus.setItem(0, 2, QTableWidgetItem(current_time))
                        
    def Add_1(self):
        row = 0
        self.status_1.insertRow(self.row_count_1)
        self.status_1.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_1.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_1.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        
        self.changeQR1Color()


    def Add_2(self):
        row = 0
        self.status_2.insertRow(self.row_count_2)
        self.status_2.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_2.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_2.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.changeQR2Color()

        
    def Add_3(self):
        row = 0
        self.status_3.insertRow(self.row_count_3)
        self.status_3.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_3.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_3.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.changeQR3Color()

        
    def Add_4(self):
        row = 0
        self.status_4.insertRow(self.row_count_4)
        self.status_4.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_4.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_4.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.changeQR4Color()

    def Add_5(self):
        row = 0
        self.status_5.insertRow(self.row_count_5)
        self.status_5.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_5.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_5.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.changeQR5Color()



        
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
        

            


        
        
        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())