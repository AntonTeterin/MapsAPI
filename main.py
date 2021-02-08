import sys
import requests
from io import BytesIO
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image, ImageQt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Карта')
        self.mainlayout = QHBoxLayout(self)

        self.image = QLabel()
        self.mainlayout.addWidget(self.image)

    def set_image(self, img):
        self.ImageQt = ImageQt.ImageQt(Image.open(img))
        self.image.setPixmap(QPixmap.fromImage(self.ImageQt))


def main():
	toponym_longitude, toponym_lattitude = '10', '50'
	delta = '20'

	map_params = {
		'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
	    'll': ",".join([toponym_longitude, toponym_lattitude]),
	    'spn': ",".join([delta, delta]),
	    'l': "map"
	}

	map_url = "http://static-maps.yandex.ru/1.x/"
	response = requests.get(map_url, params=map_params)
	window.show()
	window.set_image(BytesIO(response.content))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    main()
    sys.exit(app.exec())