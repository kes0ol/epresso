import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QHeaderView, QTableWidgetItem, QDialog, QMessageBox

from ui_addEditCoffeeForm import Ui_Dialog
from ui_main import Ui_MainWindow

ROAST = [
    "легкая",
    "светлая",
    "средняя",
    "темная",
    "сильная"
]

IS_BEAN = [
    "молотый",
    "в зернах"
]


class AddUpdateRecord(QDialog, Ui_Dialog):
    def __init__(self, window_title, title="", roast=0, is_bean=0, description="", price=0, volume=0):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(window_title)
        self.add_button.setText(window_title)
        self.init_ui()
        self.title_edit.setText(title)
        self.roast_cbox.setCurrentIndex(roast)
        self.is_bean_cbox.setCurrentIndex(is_bean)
        self.description_edit.setPlainText(description)
        self.price_box.setValue(int(price))
        self.price_cop_box.setValue(int((price - int(price)) * 100))
        self.volume_box.setValue(volume)

    def init_ui(self):
        self.add_button.clicked.connect(self.accept)


class QTableWidgetItemWithData(QTableWidgetItem):
    def __init__(self, data, *args):
        super().__init__(*args)
        self.data = data
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)


class Espresso(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def add_button_clicked(self):
        aur = AddUpdateRecord("Добавить")
        if aur.exec():
            title = aur.title_edit.text()
            roast = aur.roast_cbox.currentIndex()
            is_bean = aur.is_bean_cbox.currentIndex()
            description = aur.description_edit.toPlainText()
            price = aur.price_box.value() + (aur.price_cop_box.value() / 100)
            volume = aur.volume_box.value()
            con = sqlite3.connect("data/coffee.sqlite")
            con.cursor().execute("INSERT INTO coffee (title, roast, is_bean, description, price, volume) "
                                 "VALUES (?, ?, ?, ?, ?, ?)",
                                 (title, roast, is_bean, description, price, volume))
            con.commit()
            self.load_table()

    def update_button_clicked(self):
        si = self.table.selectedItems()
        if si:
            data = si[0].data
            aur = AddUpdateRecord("Изменить", *data[1:])

            if aur.exec():
                id = data[0]
                title = aur.title_edit.text()
                roast = aur.roast_cbox.currentIndex()
                is_bean = aur.is_bean_cbox.currentIndex()
                description = aur.description_edit.toPlainText()
                price = aur.price_box.value() + (aur.price_cop_box.value() / 100)
                volume = aur.volume_box.value()
                con = sqlite3.connect("data/coffee.sqlite")
                con.cursor().execute("UPDATE coffee SET title = ?, roast = ?, is_bean = ?, description = ?, "
                                     "price = ?, volume = ? WHERE id = ?",
                                     (title, roast, is_bean, description, price, volume, id))
                con.commit()
                self.load_table()

    def remove_button_clicked(self):
        si = self.table.selectedItems()
        if si:
            id = si[0].data[0]

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Удалить?")
            dlg.setText("Вы точно хотите удалить эту запись?")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if dlg.exec() == QMessageBox.StandardButton.Ok:
                con = sqlite3.connect("data/coffee.sqlite")
                con.cursor().execute("DELETE FROM coffee WHERE id = ?", (id,))
                con.commit()
                self.load_table()

    def init_ui(self):
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.add_button.clicked.connect(self.add_button_clicked)
        self.update_button.clicked.connect(self.update_button_clicked)
        self.remove_button.clicked.connect(self.remove_button_clicked)
        self.load_table()

    def create_table(self):
        sqlite3.connect("data/coffee.sqlite").cursor().execute(
            """CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            roast INTEGER NOT NULL,
            is_bean INTEGER NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            volume INTEGER NOT NULL
            )""")

    def load_table(self):
        self.create_table()
        for i in range(self.table.rowCount()):
            self.table.removeRow(0)
        cursor = sqlite3.connect("data/coffee.sqlite").cursor()
        cursor.execute("SELECT * FROM coffee c ORDER BY c.id")
        for i in cursor.fetchall():
            ti = [t for t in i]
            ti[2] = ROAST[int(ti[2])]
            ti[3] = IS_BEAN[int(ti[3])]
            pos = self.table.rowCount()
            self.table.insertRow(pos)
            for j in range(len(i)):
                self.table.setItem(pos, j, QTableWidgetItemWithData(i, str(ti[j])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())
