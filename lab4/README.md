#Сохранение Canvas по таймеру (PyQt5 + QML)

Приложение-рисовалка на QML (frontend) с backend-логикой на PyQt5.
Класс `Interface` каждые 5 секунд сохраняет содержимое области рисования
(`Canvas`) в PNG-файл в папке `saves/`. При закрытии приложения сохраняется
последний кадр. Статус сохранения отображается в QML внизу окна.

## Файлы
- `main.py` — backend: `Interface(QObject)`, `QTimer`, сохранение Canvas.
- `mainWindow.qml` — frontend: панель инструментов, `Canvas`, статус-бар.
- `Circle.qml`, `Square.qml` — элементы выбора толщины и цвета.

## Как работает сохранение
1. После загрузки QML `Interface.attach_engine()` находит `Canvas`
   по `objectName: "canvas"` и запускает `QTimer` (5000 мс).
2. По таймеру вызывается `QMetaObject.invokeMethod(canvas, "save", ...)` —
   встроенный QML-метод `Canvas.save(filename)` пишет содержимое в PNG.
3. Имя файла: `canvas_YYYY-MM-DD_HH-MM-SS.png` в папке `saves/`.
4. Статус сохраняется в `pyqtProperty(str)` `lastSaveStatus` и отображается
   в QML через binding `text: _backend.lastSaveStatus`.