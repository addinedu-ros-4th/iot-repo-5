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


from_class = uic.loadUiType("IoT.ui")[0]
import pandas as pd
#import atexit
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
        self.place = "0"
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
        self.btnExport.clicked.connect(self.exportTable)
        self.btnReset.clicked.connect(self.reset)
        
        self.row_count_1 = self.status_1.rowCount()
        self.row_count_2 = self.status_2.rowCount()
        self.row_count_3 = self.status_3.rowCount()
        self.row_count_4 = self.status_4.rowCount()
        self.row_count_5 = self.status_5.rowCount()
        self.LiveStatus.insertRow(0)


        self.sensor_thread = Sensor(self)
        self.sensor_thread.update.connect(self.handle_sensor_data)
        
        self.cols = ['Date', 'Temperature (°C)', 'Humidity (%)', 'Co2 (ppm)', 'PM-10 (μg/m3)', 'Place']

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
        self.sensor_thread.running = True
        self.sensor_thread.start()

    def SensorStop(self):
        self.sensor_thread.running = False
        
        """try:
            #atexit.register(self.sensor_thread.py_serial.close())
            self.sensor_thread.py_serial.close()
        except Exception as e:
            print(e)"""
            
        
    def handle_sensor_data(self, data):
        # Process the received sensor data here
        temperature_match = re.search(r'Temperature: (\d+\.\d+)°C', data)
        humidity_match = re.search(r'Humidity: (\d+\.\d+)%', data)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        temperature = None  # 미리 변수를 정의해줌
        humidity = None     # 미리 변수를 정의해줌
        if temperature_match and humidity_match:
            temperature = float(temperature_match.group(1))
            humidity = float(humidity_match.group(1))

        self.LiveStatus.setItem(0, 0, QTableWidgetItem(current_time))
        self.LiveStatus.setItem(0, 1, QTableWidgetItem(str(temperature)))
        self.LiveStatus.setItem(0, 2, QTableWidgetItem(str(humidity)))
        self.LiveStatus.setItem(0, 3, QTableWidgetItem("0"))
        self.LiveStatus.setItem(0, 4, QTableWidgetItem("0"))
        self.LiveStatus.setItem(0, 5, QTableWidgetItem(self.place))
                        
    def Add_1(self):
        self.status_1.insertRow(self.row_count_1)
        self.status_1.setItem(self.row_count_1, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_1.setItem(self.row_count_1, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_1.setItem(self.row_count_1, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text())) 
        self.status_1.setItem(self.row_count_1, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_1.setItem(self.row_count_1, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "1"

        self.changeQR1Color()


    def Add_2(self):
        self.status_2.insertRow(self.row_count_2)
        self.status_2.setItem(self.row_count_2, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_2.setItem(self.row_count_2, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_2.setItem(self.row_count_2, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_2.setItem(self.row_count_2, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_2.setItem(self.row_count_2, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "2"

        
        self.changeQR2Color()

        
    def Add_3(self):
        self.status_3.insertRow(self.row_count_3)
        self.status_3.setItem(self.row_count_3, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_3.setItem(self.row_count_3, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_3.setItem(self.row_count_3, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_3.setItem(self.row_count_3, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_3.setItem(self.row_count_3, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "3"

        
        self.changeQR3Color()

        
    def Add_4(self):
        self.status_4.insertRow(self.row_count_4)
        self.status_4.setItem(self.row_count_4, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_4.setItem(self.row_count_4, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_4.setItem(self.row_count_4, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_4.setItem(self.row_count_4, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_4.setItem(self.row_count_4, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "4"

        
        self.changeQR4Color()

    def Add_5(self):
        self.status_5.insertRow(self.row_count_5)
        self.status_5.setItem(self.row_count_5, 0, QTableWidgetItem(self.LiveStatus.item(0, 0).text()))
        self.status_5.setItem(self.row_count_5, 1, QTableWidgetItem(self.LiveStatus.item(0, 1).text()))
        self.status_5.setItem(self.row_count_5, 2, QTableWidgetItem(self.LiveStatus.item(0, 2).text()))  
        self.status_5.setItem(self.row_count_5, 3, QTableWidgetItem(self.LiveStatus.item(0, 3).text()))
        self.status_5.setItem(self.row_count_5, 4, QTableWidgetItem(self.LiveStatus.item(0, 4).text())) 
        self.place = "5"

        
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