import sys
import requests
from io import BytesIO

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PIL import Image, ImageQt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Карта')
        self.mainlayout = QHBoxLayout(self)
        self.layout1 = QVBoxLayout()

        self.radiobtn1 = QRadioButton('Карта')
        self.radiobtn1.setChecked(True)
        self.radiobtn1.clicked.connect(self.set_mode)
        self.layout1.addWidget(self.radiobtn1)

        self.radiobtn2 = QRadioButton('Спутник')
        self.radiobtn2.clicked.connect(self.set_mode)
        self.layout1.addWidget(self.radiobtn2)

        self.radiobtn3 = QRadioButton('Гибрид')
        self.radiobtn3.clicked.connect(self.set_mode)
        self.layout1.addWidget(self.radiobtn3)

        self.mainlayout.addLayout(self.layout1)
        self.image = QLabel()
        self.mainlayout.addWidget(self.image)

        self.longitude = 10
        self.lattitude = 50
        self.delta = 20
        self.mode = 'map'
        self.new_map = True
        self.update()

    def set_mode(self):
        if self.radiobtn1.isChecked():
            self.mode = 'map'
        elif self.radiobtn2.isChecked():
            self.mode = 'sat'
        elif self.radiobtn3.isChecked():
            self.mode = 'sat,skl'
        self.new_map = True
        self.update()

    def set_image(self, img):
        self.ImageQt = ImageQt.ImageQt(Image.open(img))
        self.image.setPixmap(QPixmap.fromImage(self.ImageQt))

    def paintEvent(self, event):
        if self.new_map:
            self.new_map = False
            map_url = 'http://static-maps.yandex.ru/1.x/'
            map_params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'll': ','.join([str(self.longitude), str(self.lattitude)]),
            'spn': ','.join([str(self.delta), str(self.delta)]),
            'l': self.mode,
            'size': '450,450'
            }
            response = requests.get(map_url, params=map_params)
            self.set_image(BytesIO(response.content))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.delta <= 40:
                self.delta = self.delta * 2
        if event.key() == Qt.Key_PageDown:
            if self.delta >= 0.01:
                self.delta = self.delta / 2
        if event.key() == Qt.Key_Right:
            self.longitude += self.delta * 2
            if self.longitude >= 180:
                self.longitude -= 360
        if event.key() == Qt.Key_Left:
            self.longitude -= self.delta * 2
            if self.longitude < -180:
                self.longitude += 360
        if event.key() == Qt.Key_Up:
            self.lattitude += self.delta * 2
            if self.lattitude + self.delta > 90:
                self.lattitude = 90 - self.delta
        if event.key() == Qt.Key_Down:
            self.lattitude -= self.delta * 2
            if self.lattitude - self.delta < -90:
                self.lattitude = -90 + self.delta
        self.new_map = True
        self.update()

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())