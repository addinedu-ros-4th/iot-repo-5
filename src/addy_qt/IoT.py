import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from datetime import datetime


from_class = uic.loadUiType("IoT.ui")[0]
import pandas as pd


class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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


    def Add_1(self):
        row = 0
        self.status_1.insertRow(self.row_count_1)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        self.LiveStatus.setItem(row, 0, QTableWidgetItem("1"))
        self.LiveStatus.setItem(row, 1, QTableWidgetItem("2"))
        self.LiveStatus.setItem(row, 2, QTableWidgetItem(current_time))
        self.status_1.setItem(self.row_count_1, 0, QTableWidgetItem("1"))
        self.status_1.setItem(self.row_count_1, 1, QTableWidgetItem("2"))
        self.status_1.setItem(self.row_count_1, 2, QTableWidgetItem(current_time))
        
        self.changeQR1Color()


    def Add_2(self):
        row = 0
        self.status_2.insertRow(self.row_count_2)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        self.LiveStatus.setItem(row, 0, QTableWidgetItem("2"))
        self.LiveStatus.setItem(row, 1, QTableWidgetItem("2"))
        self.LiveStatus.setItem(row, 2, QTableWidgetItem(current_time))
        self.status_2.setItem(self.row_count_2, 0, QTableWidgetItem("2"))
        self.status_2.setItem(self.row_count_2, 1, QTableWidgetItem("2"))
        self.status_2.setItem(self.row_count_2, 2, QTableWidgetItem(current_time))
        self.changeQR2Color()

        
    def Add_3(self):
        row = 0
        self.status_3.insertRow(self.row_count_3)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        self.LiveStatus.setItem(row, 0, QTableWidgetItem("3"))
        self.LiveStatus.setItem(row, 1, QTableWidgetItem("2"))
        self.LiveStatus.setItem(row, 2, QTableWidgetItem(current_time))
        self.status_3.setItem(self.row_count_3, 0, QTableWidgetItem("3"))
        self.status_3.setItem(self.row_count_3, 1, QTableWidgetItem("2"))
        self.status_3.setItem(self.row_count_3, 2, QTableWidgetItem(current_time))
        self.changeQR3Color()

        
    def Add_4(self):
        row = 0
        self.status_4.insertRow(self.row_count_4)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        self.LiveStatus.setItem(row, 0, QTableWidgetItem("4"))
        self.LiveStatus.setItem(row, 1, QTableWidgetItem("2"))
        self.LiveStatus.setItem(row, 2, QTableWidgetItem(current_time))
        self.status_4.setItem(self.row_count_4, 0, QTableWidgetItem("4"))
        self.status_4.setItem(self.row_count_4, 1, QTableWidgetItem("2"))
        self.status_4.setItem(self.row_count_4, 2, QTableWidgetItem(current_time))
        self.changeQR4Color()

    def Add_5(self):
        row = 0
        self.status_5.insertRow(self.row_count_5)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        self.LiveStatus.setItem(row, 0, QTableWidgetItem("5"))
        self.LiveStatus.setItem(row, 1, QTableWidgetItem("2"))
        self.LiveStatus.setItem(row, 2, QTableWidgetItem(current_time))
        self.status_5.setItem(self.row_count_5, 0, QTableWidgetItem("5"))
        self.status_5.setItem(self.row_count_5, 1, QTableWidgetItem("2"))
        self.status_5.setItem(self.row_count_5, 2, QTableWidgetItem(current_time))    
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