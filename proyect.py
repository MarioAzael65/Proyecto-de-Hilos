# Importer bibliophiles
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QLineEdit, QPushButton, QLabel, QDialog, QMessageBox, QTextEdit
import requests
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
import requests


# Subclass QMainWindow

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My_Browser")
        self.resize(740, 520)
        self.container = QWidget()
        self.lyt_main = QGridLayout()

        self.lnedt_Text = QLineEdit()
        self.btn_search = QPushButton("Search")
        self.btn_search.clicked.connect(self.add_text)

        self.lyt_main.addWidget(self.lnedt_Text, 0, 0)
        self.lyt_main.addWidget(self.btn_search, 0, 1)

        self.container.setLayout(self.lyt_main)
        self.setMenuWidget(self.container)

        self.container2 = QWidget()
        self.lyt_main2 = QGridLayout()

        left_column = QWidget()
        center_column = QWidget()
        right_column = QWidget()

        self.lyt_main2.addWidget(left_column, 0, 0)
        self.lyt_main2.addWidget(center_column, 0, 1)
        self.lyt_main2.addWidget(right_column, 0, 2)

        self.container2.setLayout(self.lyt_main2)
        self.setCentralWidget(self.container2)

    def add_text(self):
        words = []
        list = self.lnedt_Text.text()
        for words in list:
            words = list.split(",")
        for i in words:
            self.get_movies(i)

    def get_movies(self, palabra):
        url_services = "http://clandestina-hds.com:80/movies/title?search="
        r = requests.get(url_services + palabra)
        movies_data = r.json()
        index = 0
        limit = 3
        for movie in movies_data['results']:
            self.show_image(movie["image"])
            index = index + 1
            if index == limit:
                break

    def show_info(self, title):
        info = QTextEdit()
        info.loadFromData(requests.get(title).content)

    def show_image(self, url_image):
        image = QImage()
        image.loadFromData(requests.get(url_image).content)
        pixel = QPixmap.fromImage(image).scaled(319, 474)
        self.image_label = QLabelClickable(self)
        self.image_label.setPixmap(QPixmap(pixel))
        self.image_label.show()
        self.image_label.setCursor(Qt.PointingHandCursor)
        self.image_label.clicked.connect(self.Clic)

        self.lyt_main2.addWidget(self.image_label)
        self.container2.setLayout(self.lyt_main2)
        self.setCentralWidget(self.container2)

    def Clic(self):
        QMessageBox.information(self, "info",
                                "Pelicula:")


class QLabelClickable(QLabel):
    clicked = pyqtSignal(str)

    def _init_(self, parent=None):
        super(QLabelClickable, self)._init_(parent)

    def mousePressEvent(self, event):
        self.ultimo = "Clic"

    def mouseReleaseEvent(self, event):
        if self.ultimo == "Clic":
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)

    def performSingleClickAction(self):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)


app = QApplication([])
window = Main()
window.show()
app.exec_()
