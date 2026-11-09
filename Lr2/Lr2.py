import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit
)
from PyQt5.QtCore import pyqtSignal, Qt


class CurrencyConverter(QWidget):

    #имя поля-источника ("USD" / "RUB" / "EUR").
    valueChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()


        self.rate_usd = 90.0    
        self.rate_eur = 100.0 

        layout = QVBoxLayout(self)

  
        row_usd = QHBoxLayout()
        row_usd.addWidget(QLabel("Доллар (USD):"))
        self.edit_usd = QLineEdit("1.00")
        self.edit_usd.setAlignment(Qt.AlignRight)
        row_usd.addWidget(self.edit_usd)
        layout.addLayout(row_usd)

        
        row_rub = QHBoxLayout()
        row_rub.addWidget(QLabel("Рубль (RUB):"))
        self.edit_rub = QLineEdit("90.00")
        self.edit_rub.setAlignment(Qt.AlignRight)
        row_rub.addWidget(self.edit_rub)
        layout.addLayout(row_rub)

        row_eur = QHBoxLayout()
        row_eur.addWidget(QLabel("Евро (EUR):"))
        self.edit_eur = QLineEdit("0.90")
        self.edit_eur.setAlignment(Qt.AlignRight)
        row_eur.addWidget(self.edit_eur)
        layout.addLayout(row_eur)

        layout.addSpacing(10)

        #Метка-журнал (обновляется через собственный сигнал)
        self.log_label = QLabel("")
        layout.addWidget(self.log_label)

        #Подсказка
        hint = QLabel("Измените любое поле — остальные обновятся")
        hint.setStyleSheet("color: gray; font-size: 12px;")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        layout.addStretch()

        #ПОДКЛЮЧЕНИЕ СИГНАЛОВ К СЛОТАМ
        self.edit_usd.textChanged.connect(self.on_usd_changed)
        self.edit_rub.textChanged.connect(self.on_rub_changed)
        self.edit_eur.textChanged.connect(self.on_eur_changed)

        #к слоту-журналу.
        self.valueChanged.connect(self.log_change)



    def on_usd_changed(self, _text: str):
        usd = self._get_float(self.edit_usd)
        if usd is None:
            return
        rub = usd * self.rate_usd
        eur = rub / self.rate_eur
        
        self._set_silently(self.edit_rub, f"{rub:.2f}")
        self._set_silently(self.edit_eur, f"{eur:.2f}")
        
        self.valueChanged.emit("USD")

    def on_rub_changed(self, _text: str):
        rub = self._get_float(self.edit_rub)
        if rub is None:
            return
        usd = rub / self.rate_usd
        eur = rub / self.rate_eur
        self._set_silently(self.edit_usd, f"{usd:.2f}")
        self._set_silently(self.edit_eur, f"{eur:.2f}")
        self.valueChanged.emit("RUB")

    def on_eur_changed(self, _text: str):
        eur = self._get_float(self.edit_eur)
        if eur is None:
            return
        rub = eur * self.rate_eur
        usd = rub / self.rate_usd
        self._set_silently(self.edit_rub, f"{rub:.2f}")
        self._set_silently(self.edit_usd, f"{usd:.2f}")
        self.valueChanged.emit("EUR")

    def log_change(self, source: str):
        self.log_label.setText(f"Журнал: последнее изменение — {source}")

    

    @staticmethod
    def _get_float(line_edit: QLineEdit):
        """Безопасно достать float из поля. None, если текст не число."""
        text = line_edit.text().replace(",", ".").strip()
        try:
            return float(text)
        except ValueError:
            return None

    @staticmethod
    def _set_silently(line_edit: QLineEdit, value: str):
        line_edit.blockSignals(True)
        line_edit.setText(value)
        line_edit.blockSignals(False)


class Lab2Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная 2 — Сигналы и слоты")
        self.resize(420, 260)
        self.setCentralWidget(CurrencyConverter())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Lab2Window()
    window.show()
    sys.exit(app.exec_())