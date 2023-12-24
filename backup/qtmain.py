# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtCore import Qt
# import pandas as pd
# import numpy as np
# class TableModel(QtCore.QAbstractTableModel):
#     def __init__(self, data):
#         super(TableModel, self).__init__()
#         self._data = data
#
#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             # See below for the nested-list data structure.
#             # .row() indexes into the outer list,
#             # .column() indexes into the sub-list
#             return self._data[index.row()][index.column()]
#
#     def rowCount(self, index):
#         # The length of the outer list.
#         return len(self._data)
#
#     def columnCount(self, index):
#         # The following takes the first sub-list, and returns
#         # the length (only works if all rows are an equal length)
#         return len(self._data[0])
#
#
# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.table = window.tableWidget
#
#         data = np.array(pd.read_csv('result.csv'))
#
#         self.model = TableModel(data)
#         self.table.setModel(self.model)
#
#         self.setCentralWidget(self.table)
#
#
# app=QtWidgets.QApplication(sys.argv)
#
# window = uic.loadUi("sonuclar.ui")
# data = np.array(pd.read_csv('h_df.csv'))
# window.label.setText(str(data.shape))
#
# model = TableModel(data)
# window.tableWidget.setRowCount(len(data))
# window.tableWidget.setColumnCount(len(data[0]))
# window.tableWidget.setModel(model)
#
# for i in range(len(data)):
#     for j in range(len(data[0])):
#         window.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
#
#
# # window=MainWindow()
# window.show()
# app.exec_()

import sys
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableView, qApp
from PyQt5.QtCore import QAbstractTableModel, Qt
import time
df = pd.read_csv("w_df.csv")

STATUS = ["Veriler yükleniyor...", "Veriler yüklendi.", "NMF başlatılıyor...", "NMF başlatıldı.", "NMF tamamlandı.",
            "Sonuçlar kaydediliyor...", "Sonuçlar kaydedildi.", "Sonuçlar yükleniyor...", "Sonuçlar yüklendi."]

class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

def load_h():
    df = pd.read_csv("h_df.csv")
    df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
    model = pandasModel(df)
    view.setModel(model)
    win.label.setText(f"h matrisi boyutu: {df.shape}")

def load_w():
    df = pd.read_csv("w_df.csv")
    df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
    model = pandasModel(df)
    view.setModel(model)
    win.label.setText(f"w matrisi boyutu: {df.shape}")

def load_result():
    df = pd.read_csv("result.csv")
    df.set_index('Unnamed: 0', inplace=True)
    model = pandasModel(df)
    view.setModel(model)
    win.label.setText(f"Sonuç;")
def open_other_ui():
    win.label.setText("Boş")
    # view.setModel(model)
    win.h_buton.clicked.connect(load_h)
    win.w_buton.clicked.connect(load_w)
    win.result_buton.clicked.connect(load_result)
    win.show()


def start_nmf():
    qApp.processEvents()
    time.sleep(1)
    for i in range(len(STATUS)):
        qApp.processEvents()
        time.sleep(1)
        win2.plainTextEdit.setPlainText(win2.plainTextEdit.toPlainText() + "\n" + STATUS[i])
        win2.plainTextEdit.moveCursor(win2.plainTextEdit.textCursor().End)
    qApp.processEvents()
    win2.plainTextEdit.setPlainText(win2.plainTextEdit.toPlainText() + "\n" + "\n" + "Bitti.")
    win2.plainTextEdit.moveCursor(win2.plainTextEdit.textCursor().End)
def nmf_ekrani():
    print("nmf ekrani")
    win2.show()
    win2.plainTextEdit.setPlainText("Hazır." + "\n")
    win2.start_buton.clicked.connect(start_nmf)

def tahmin_ekrani():
    print("tahmin ekrani")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # model = pandasModel(df)
    win1 = uic.loadUi("main.ui")
    win1.setWindowTitle("Ana Pencere")
    win1.sonuclar_buton.clicked.connect(open_other_ui)
    win1.nmf_buton.clicked.connect(nmf_ekrani)
    win2 = uic.loadUi("NMF.ui")
    win1.tahmin_buton.clicked.connect(tahmin_ekrani)
    win = uic.loadUi("sonuclar.ui")
    win.setWindowTitle("Sonuçlar")

    view = win.tableView

    # # view.setModel(model)
    # win.h_buton.clicked.connect(load_h)
    # win.w_buton.clicked.connect(load_w)

    win1.show()
    app.exec()
