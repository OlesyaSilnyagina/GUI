import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTabWidget, QTableView,
    QFileDialog, QMessageBox, QInputDialog
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import Qt


CONNECTION_NAME = "lr3_connection"


class Lab3Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лр3 — Таблицы и SQL")
        self.resize(800, 500)

        self.db = None  
        self._tab_counter = 0  

        self._build_menu()
        self._build_ui()
        self._set_controls_enabled(False)

    

    def _build_menu(self):
        menu = self.menuBar().addMenu("База данных")

        act_set = menu.addAction("Set connection")
        act_set.triggered.connect(self.on_set_connection)

        act_close = menu.addAction("Close connection")
        act_close.triggered.connect(self.on_close_connection)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

    
        top = QHBoxLayout()

        top.addWidget(QLabel("Таблица:"))
        self.combo_tables = QComboBox()
        self.combo_tables.setMinimumWidth(200)
        self.combo_tables.currentIndexChanged.connect(self.on_table_selected)
        top.addWidget(self.combo_tables)

        top.addSpacing(10)

        self.btn1 = QPushButton("bt1: имена объектов")
        self.btn1.clicked.connect(self.on_bt1)
        top.addWidget(self.btn1)

        self.btn2 = QPushButton("bt2: типы и имена")
        self.btn2.clicked.connect(self.on_bt2)
        top.addWidget(self.btn2)

        self.btn3 = QPushButton("bt3: DDL таблиц")
        self.btn3.clicked.connect(self.on_bt3)
        top.addWidget(self.btn3)

        self.btn_custom = QPushButton("Свой SQL")
        self.btn_custom.clicked.connect(self.on_custom_sql)
        top.addWidget(self.btn_custom)

        top.addStretch()
        layout.addLayout(top)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

    def _set_controls_enabled(self, enabled: bool):
        for w in (self.combo_tables, self.btn1, self.btn2,
                  self.btn3, self.btn_custom):
            w.setEnabled(enabled)


    def on_set_connection(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл базы данных SQLite",
            "",
            "SQLite DB (*.db *.sqlite *.sqlite3);;Все файлы (*)"
        )
        if not path:
            return

        if self.db is not None:
            self.on_close_connection()

        self.db = QSqlDatabase.addDatabase("QSQLITE", CONNECTION_NAME)
        self.db.setDatabaseName(path)

        if not self.db.open():
            QMessageBox.critical(
                self, "Ошибка",
                "Не удалось открыть базу данных:\n"
                + self.db.lastError().text()
            )
            QSqlDatabase.removeDatabase(CONNECTION_NAME)
            self.db = None
            return

        self._set_controls_enabled(True)

        
        self._add_query_tab(
            "sqlite_master",
            "SELECT * FROM sqlite_master"
        )

        
        self._fill_tables_combo()

    

    def on_close_connection(self):
        
        self.tabs.clear()
        self.combo_tables.clear()
        self._tab_counter = 0

        # Закрываем и удаляем соединение
        if self.db is not None:
            self.db.close()
            self.db = None
        if QSqlDatabase.contains(CONNECTION_NAME):
            QSqlDatabase.removeDatabase(CONNECTION_NAME)

        self._set_controls_enabled(False)


    def on_bt1(self):
        self._add_query_tab(
            "bt1: имена",
            "SELECT name FROM sqlite_master"
        )

    def on_bt2(self):
        self._add_query_tab(
            "bt2: типы/имена",
            "SELECT type, name FROM sqlite_master"
        )

    def on_bt3(self):
        self._add_query_tab(
            "bt3: DDL",
            "SELECT name, sql FROM sqlite_master WHERE type='table'"
        )

    def on_table_selected(self, index: int):
        if index < 0:
            return
        table = self.combo_tables.itemText(index)
        if not table:
            return

        self._add_query_tab(
            f"Таблица: {table}",
            f'SELECT * FROM "{table}"'
        )

    def on_custom_sql(self):
        sql, ok = QInputDialog.getMultiLineText(
            self,
            "Свой SQL-запрос",
            "Введите SQL-запрос:",
            "SELECT name, type FROM sqlite_master;"
        )
        if not ok or not sql.strip():
            return

        self._add_query_tab("Свой SQL", sql.strip())


    def _fill_tables_combo(self):
        self.combo_tables.blockSignals(True)
        self.combo_tables.clear()

        query = QSqlQuery(self.db)
        query.exec_("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                    "ORDER BY name")

        while query.next():
            self.combo_tables.addItem(query.value(0))

        self.combo_tables.blockSignals(False)
        self.combo_tables.setCurrentIndex(-1)  # ничего не выбрано

    def _add_query_tab(self, title: str, sql: str):
        model = QSqlQueryModel(self)
        model.setQuery(sql, self.db)

        if model.lastError().isValid():
            QMessageBox.warning(
                self, "Ошибка запроса",
                f"Запрос:\n{sql}\n\nОшибка:\n{model.lastError().text()}"
            )
            return

        view = QTableView()
        view.setModel(model)
        view.resizeColumnsToContents()

        self._tab_counter += 1
        self.tabs.addTab(view, f"Tab{self._tab_counter}: {title}")
        self.tabs.setCurrentWidget(view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Lab3Window()
    window.show()
    sys.exit(app.exec_())