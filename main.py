from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import sys
import os

class Lab1Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная 1")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("Нажми на кнопку  и увидишь предсказание на день")
        self.label.setStyleSheet("font-size: 16px; qproperty-alignment: AlignCenter;")
        layout.addWidget(self.label)

        # Кнопка
        self.button = QPushButton("Мое предсказание")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.image = "im.png"

    def on_button_click(self):
        if not os.path.exists(self.image):
            self.label.setText("Файл изображения не найден!\nПоложите im.png в папку")
            return

        # Загружаем изображение
        pixmap = QPixmap(self.image)
        if pixmap.isNull():
            self.label.setText("Не удалось загрузить изображение\nПроверьте формат")
            return

        scaled_pixmap = pixmap.scaled(self.label.size(), aspectRatioMode=1) 
        self.label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Lab1Window()
    window.show()
    sys.exit(app.exec_())
