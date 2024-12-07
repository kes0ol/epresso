import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QHeaderView, QTableWidgetItem


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.init_ui()

    def init_ui(self):
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.load_table()

    def create_table(self):
        sqlite3.connect("coffee.sqlite").cursor().execute(
            """CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            roast TEXT NOT NULL,
            is_bean INTEGER NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            volume INTEGER NOT NULL
            )""")

    def load_table(self):
        self.create_table()
        cursor = sqlite3.connect("coffee.sqlite").cursor()
        cursor.execute("SELECT * FROM coffee c ORDER BY c.id")
        for i in cursor.fetchall():
            pos = self.table.rowCount()
            self.table.insertRow(pos)
            i = list(i)
            i[3] = "в зернах" if i[3] else "молотый"
            for j in range(len(i)):
                self.table.setItem(pos, j, QTableWidgetItem(str(i[j])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())
