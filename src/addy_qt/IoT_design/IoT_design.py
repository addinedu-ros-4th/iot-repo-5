import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt  



from_class = uic.loadUiType("IoT_design.ui")[0]




class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 배경 이미지 설정
        background_image_path = "image/background.png"
        self.background_pixmap = QPixmap(background_image_path)

        # "map" QLabel에 이미지 설정
        map_image_path = "image/map.png"
        map_pixmap = QPixmap(map_image_path)
        self.map_label.setPixmap(map_pixmap)
        self.map_label.setScaledContents(True)

        logo_image_path = "image/logo.png"
        logo_pixmap = QPixmap(logo_image_path)
        self.camera.setPixmap(logo_pixmap)
        self.camera.setAlignment(Qt.AlignCenter)


        # "btnplot" 버튼의 배경으로 이미지 설정
        plot_image_path = "image/plot.png"
        plot_pixmap = QPixmap(plot_image_path)
        self.btnplot.setStyleSheet("background-image: url({}); background-repeat: no-repeat; background-position: center;".format(plot_image_path))
        self.btnplot.setIconSize(plot_pixmap.size())
        
        # btnExport 버튼에 이미지 설정 및 크기 조절
        export_image_path = "image/export_to_csv.png"
        export_pixmap = QPixmap(export_image_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.btnExport.setIcon(QIcon(export_pixmap))
        self.btnExport.setIconSize(export_pixmap.size())
        
        # btnReset 버튼에 이미지 설정 및 크기 조절
        reset_image_path = "image/delete.png"
        reset_pixmap = QPixmap(reset_image_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.btnReset.setIcon(QIcon(reset_pixmap))
        self.btnReset.setIconSize(reset_pixmap.size())
         
        # status label에 이미지 설정
        status_image_path = "image/status_great.png"
        status_pixmap = QPixmap(status_image_path)
        self.status_label.setPixmap(status_pixmap)
        self.status_label.setScaledContents(True)
        
        
        self.test.clicked.connect(self.add_row_to_table)
        self.robot_angle.valueChanged.connect(self.update_angle_value)
        
        
        
    #QR_X 입력 시 해당 위치에 image/place.png 표시
    #status label에 text feedback 말고 image 안에 있는 이미지 활용하여 상태 표시

    def update_angle_value(self, value):
        # 다이얼의 값이 변경될 때마다 angle 텍스트 상자에 해당 값을 표시
        self.angle.setText(str((value-50)*(-1)))
        
    def add_row_to_table(self):
        # 새로운 행 생성
        row_position = self.status_1.rowCount()
        self.status_1.insertRow(row_position)
        
        # 각 셀에 0 추가
        column_count = self.status_1.columnCount()
        for column in range(column_count):
            item = QTableWidgetItem("0")
            self.status_1.setItem(row_position, column, item)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.background_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
