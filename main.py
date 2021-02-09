import sys
import requests
from io import BytesIO

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


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

        self.layout1.addStretch()

        self.input_edit = QLineEdit()
        self.layout1.addWidget(self.input_edit)

        self.search_btn = QPushButton('Искать')
        self.search_btn.clicked.connect(self.search)
        self.layout1.addWidget(self.search_btn)

        self.clear_btn = QPushButton('Сброс поискового результата')
        self.clear_btn.clicked.connect(self.clear)
        self.layout1.addWidget(self.clear_btn)

        self.mainlayout.addLayout(self.layout1)
        self.image = QLabel()
        self.mainlayout.addWidget(self.image)

        self.longitude = 10
        self.lattitude = 50
        self.delta = 20
        self.mode = 'map'
        self.is_pt = False
        self.new_map = True
        self.update()

    def search(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.input_edit.text(),
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        response = response.json()["response"]["GeoObjectCollection"][
            "featureMember"]
        if not response:
            self.input_edit.setText('Ничего не найдено')
            return
        toponym = response[0]["GeoObject"]
        res = [float(x) for x in self.get_coordinates(toponym)]
        self.longitude, self.lattitude, self.delta = res
        self.is_pt = True
        self.pt_x = self.longitude
        self.pt_y = self.lattitude
        self.new_map = True
        self.update()

    def clear(self):
        self.is_pt = False
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
        image = QPixmap()
        image.loadFromData(img.getvalue())
        self.image.setPixmap(image)

    def get_coordinates(self, toponym):
        x, y = toponym["Point"]["pos"].split()
        left, down = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
        right, up = toponym["boundedBy"]["Envelope"]["upperCorner"].split()
        delta = str(abs(float(right) - float(left)))
        return x, y, delta

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
            if self.is_pt:
                map_params['pt'] = ','.join(
                    [str(self.pt_x), str(self.pt_y), 'pm2grl'])
            response = requests.get(map_url, params=map_params)
            self.set_image(BytesIO(response.content))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.delta <= 40:
                self.delta = self.delta * 2
        if event.key() == Qt.Key_PageDown:
            if self.delta >= 0.01:
                self.delta = self.delta / 2
        if event.key() == Qt.Key_D:
            self.longitude += self.delta * 2
            if self.longitude >= 180:
                self.longitude -= 360
        if event.key() == Qt.Key_A:
            self.longitude -= self.delta * 2
            if self.longitude < -180:
                self.longitude += 360
        if event.key() == Qt.Key_W:
            self.lattitude += self.delta * 2
            if self.lattitude + self.delta > 90:
                self.lattitude = 90 - self.delta
        if event.key() == Qt.Key_S:
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
