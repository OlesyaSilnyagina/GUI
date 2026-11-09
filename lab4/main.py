import os
import sys
from datetime import datetime

from PyQt5.QtCore import QObject, QUrl, QTimer, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QMetaObject, Q_ARG


SAVE_DIR = "saves"
SAVE_INTERVAL_MS = 5000  


class Interface(QObject):
    

    lastSaveStatusChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._last_save_status = "Сохранение ещё не выполнялось"
        self._canvas = None  
        self._engine = None

        
        os.makedirs(SAVE_DIR, exist_ok=True)

        self._timer = QTimer(self)
        self._timer.setInterval(SAVE_INTERVAL_MS)
        self._timer.timeout.connect(self.save_canvas)

    

    @pyqtProperty(str, notify=lastSaveStatusChanged)
    def lastSaveStatus(self):
        return self._last_save_status

    def _set_status(self, text: str):
        self._last_save_status = text
        self.lastSaveStatusChanged.emit()



    def attach_engine(self, engine):
        self._engine = engine
        roots = engine.rootObjects()
        if not roots:
            self._set_status("Ошибка: QML не загружен")
            return

        root = roots[0]
        self._canvas = root.findChild(QObject, "canvas")
        if self._canvas is None:
            self._set_status("Ошибка: Canvas не найден в QML")
            return

        self._set_status(f"Автосохранение каждые {SAVE_INTERVAL_MS // 1000} с")
        self._timer.start()


    def save_canvas(self):
        if self._canvas is None:
            self._set_status("Ошибка: Canvas не найден")
            return

        filename = datetime.now().strftime("canvas_%Y-%m-%d_%H-%M-%S.png")
        path = os.path.abspath(os.path.join(SAVE_DIR, filename))

        
        ok = QMetaObject.invokeMethod(
            self._canvas,
            "save",
            Q_ARG(str, path)
        )

        if ok:
            self._set_status(f"Сохранено: {filename}")
            print(f"[autosave] {path}")
        else:
            self._set_status("Ошибка сохранения Canvas")
            print("[autosave] Не удалось сохранить Canvas")

    

    def save_on_exit(self):
        if self._canvas is not None:
            self.save_canvas()


def main():
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)



    
    engine.load(QUrl.fromLocalFile("mainWindow.qml"))

    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    
    interface.attach_engine(engine)

    
    app.aboutToQuit.connect(interface.save_on_exit)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()