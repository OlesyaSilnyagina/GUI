# Лабораторная работа 3. Таблицы и SQL (PyQt5 + SQLite)

## Что делает
Приложение подключается к SQLite-базе через `QFileDialog`
и выводит результаты SQL-запросов в `QTableView` внутри `QTabWidget`.

- **Set connection** — выбор файла БД и подключение.
- После подключения в **Tab1** выводится `SELECT * FROM sqlite_master`.
- **bt1** — `SELECT name FROM sqlite_master` → Tab2.
- **QComboBox** — выбор таблицы, `SELECT * FROM "<таблица>"` → Tab3.
- **bt2** — `SELECT type, name FROM sqlite_master` → Tab4.
- **bt3** — `SELECT name, sql FROM sqlite_master WHERE type='table'` → Tab5.
- **Свой SQL** — модальное окно `QInputDialog` с вводом запроса → новая вкладка.
- **Close connection** — закрывает БД, удаляет соединение, очищает вкладки.
