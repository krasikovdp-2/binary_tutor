from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

import sys
from database import Database, add_tables_menu
from binary_game import BinaryGame


class Ui_StartWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(381, 226)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.binary_game_button = QtWidgets.QPushButton(self.centralwidget)
        self.binary_game_button.setObjectName("binary_game_button")
        self.verticalLayout.addWidget(self.binary_game_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Двоичный тьютор"))
        self.binary_game_button.setText(_translate("MainWindow", "Binary game"))


class StartWindow(QMainWindow, Ui_StartWindow):
    def __init__(self, db_file='db.sqlite'):
        super().__init__()
        self.setupUi(self)
        self.binary_game_button.clicked.connect(self.binary_game)
        self.db = Database(db_file)
        add_tables_menu(self, self.db)

    def open_game(self, class_):
        def inner(self_):
            game = class_(self, self.db)
            game.show()
            self.hide()
            game.closed.connect(self.show)
        return inner

    def binary_game(self):
        bg = BinaryGame(self, self.db)
        bg.show()
        self.hide()
        bg.closed.connect(self.show)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec())
