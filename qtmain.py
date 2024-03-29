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
import time

import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, qApp, QFileDialog

from nmf import NMF_model

FILE = ""
NMF_OBJ = NMF_model()
X, W, H, RESULT, nmf_done = "", "", "", "", ""


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


def load_x():
    df_X = X

    df_X.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
    model = pandasModel(df_X)
    view.setModel(model)
    sonuclar_win.label.setText(f"x matrisi boyutu: {df_X.shape}")


def load_h():
    df_h = H

    model = pandasModel(df_h)
    view.setModel(model)
    sonuclar_win.label.setText(f"h matrisi boyutu: {df_h.shape}")


def load_w():
    df_W = W

    model = pandasModel(df_W)
    view.setModel(model)
    sonuclar_win.label.setText(f"w matrisi boyutu: {df_W.shape}")


def load_result():
    global RESULT
    df_result = RESULT

    # df.set_index('Unnamed: 0', inplace=True)
    model = pandasModel(df_result)

    view.setModel(model)

    sonuclar_win.label.setText(f"Sonuç;")


def open_result_ui():
    sonuclar_win.setWindowTitle("Sonuçlar")
    # view.setModel(model)
    if nmf_done:
        sonuclar_win.h_buton.clicked.connect(load_h)
        sonuclar_win.w_buton.clicked.connect(load_w)
        sonuclar_win.x_buton.clicked.connect(load_x)
        sonuclar_win.result_buton.clicked.connect(load_result)
    else:
        sonuclar_win.label.setText("NMF işlemi henüz bitmemiş.")
    sonuclar_win.show()


def open_file():
    global FILE

    file = QFileDialog.getOpenFileName(nmf_win, 'Open file')

    only_filename = file[0].split("/")[-1]

    FILE = only_filename
    nmf_win.plainTextEdit.setPlainText("\n" + "Dosya seçildi." + "\n" + f"Seçilen dosya : {FILE}")
    nmf_win.plainTextEdit.moveCursor(nmf_win.plainTextEdit.textCursor().End)


def start_nmf():
    global X, W, H, FILE, RESULT, nmf_done
    qApp.processEvents()
    time.sleep(1)
    num_of_topics = nmf_win.topic_spin.value()
    df = pd.read_csv(str(FILE))
    X, W, H, RESULT = NMF_OBJ.NMF_func(nmf_win, df, qApp, num_of_topics)

    nmf_done = True
    qApp.processEvents()
    nmf_win.plainTextEdit.setPlainText(nmf_win.plainTextEdit.toPlainText() + "\n" + "\n" + "Bitti.")
    nmf_win.plainTextEdit.moveCursor(nmf_win.plainTextEdit.textCursor().End)


def nmf_ekrani():
    nmf_win.setWindowTitle("NMF Ekranı")
    nmf_win.show()

    nmf_win.plainTextEdit.setPlainText("Hazır." + "\n")
    nmf_win.dosya_buton.clicked.connect(open_file)
    if FILE == "":
        nmf_win.plainTextEdit.setPlainText(nmf_win.plainTextEdit.toPlainText() + "\n" + "Dosya seçilmedi.")
        nmf_win.plainTextEdit.moveCursor(nmf_win.plainTextEdit.textCursor().End)

    nmf_win.start_buton.clicked.connect(start_nmf)


def tahmin_et_func():
    cümle = tahmin_win.tahmin_line.text()

    temp2 = NMF_OBJ.tahmin_et(cümle)
    print(temp2)
    tahmin_win.cikti_plain.setPlainText(tahmin_win.cikti_plain.toPlainText() + "\n" + f"{temp2}")
    tahmin_win.cikti_plain.moveCursor(tahmin_win.cikti_plain.textCursor().End)
    tahmin_win.tahmin_line.setText("")


def tahmin_ekrani():
    tahmin_win.setWindowTitle("Tahmin Ekranı")
    tahmin_win.show()
    tahmin_win.cikti_plain.setPlainText("Hazır." + "\n")
    tahmin_win.cikti_plain.moveCursor(tahmin_win.cikti_plain.textCursor().End)

    print("wtf")
    tahmin_win.guess_buton.clicked.connect(tahmin_et_func)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # model = pandasModel(df)
    main_win = uic.loadUi("main.ui")
    nmf_win = uic.loadUi("NMF.ui")
    tahmin_win = uic.loadUi("tahmin.ui")
    sonuclar_win = uic.loadUi("sonuclar.ui")

    main_win.setWindowTitle("Ana Pencere")

    main_win.sonuclar_buton.clicked.connect(open_result_ui)
    main_win.nmf_buton.clicked.connect(nmf_ekrani)
    main_win.tahmin_buton.clicked.connect(tahmin_ekrani)

    view = sonuclar_win.tableView

    # # view.setModel(model)
    # win.h_buton.clicked.connect(load_h)
    # win.w_buton.clicked.connect(load_w)

    main_win.show()
    app.exec()
