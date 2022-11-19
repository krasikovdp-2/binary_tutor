from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

import sqlite3


def add_tables_menu(parent, db=None):
    menubar = getattr(parent, 'menubar', None)
    assert menubar
    menu = QtWidgets.QMenu(menubar)
    menu.setObjectName("menu")
    menu.setTitle('Таблицы')
    action = QtWidgets.QAction(parent)
    action.setObjectName("action")
    action.setText('Рекорды')
    action.triggered.connect(lambda *args: RecordTable(parent, db=db).show())
    action_2 = QtWidgets.QAction(parent)
    action_2.setObjectName("action_2")
    action_2.setText('Игры')
    action_2.triggered.connect(lambda *args: GamesTable(parent, db=db).show())
    menu.addAction(action)
    menu.addAction(action_2)
    menubar.addAction(menu.menuAction())
    return menu


class Ui_RecordTable(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Таблица рекордов"))
        self.lineEdit.setToolTip(_translate("MainWindow", "Ваше имя"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Ваше имя"))
        self.pushButton.setText(_translate("MainWindow", "Добавить рекорд"))


class Database:
    def __init__(self, db_file=None):
        if db_file is None:
            self.db_file = 'db.sqlite'
        else:
            self.db_file = db_file
        self.con = sqlite3.connect(self.db_file)
        if not self._check_db_schema():
            self._reset_db()

    def _check_db_schema(self):
        cur = self.con.cursor()
        games_schema = cur.execute('PRAGMA table_info(games)').fetchall()
        records_schema = cur.execute('PRAGMA table_info(records)').fetchall()
        return games_schema == [(0, 'id', 'INTEGER', 1, None, 1),
                                (1, 'title', 'STRING', 0, None, 0)] and \
               records_schema == [(0, 'id', 'INTEGER', 1, None, 1),
                                  (1, 'game', 'INTEGER', 0, None, 0),
                                  (2, 'nickname', 'STRING', 0, None, 0),
                                  (3, 'score', 'INTEGER', 0, None, 0)]

    def _reset_db(self):
        cur = self.con.cursor()
        try:
            cur.execute('DROP TABLE games')
        except sqlite3.OperationalError:  # нет такой таблицы
            pass
        try:
            cur.execute('DROP TABLE records')
        except sqlite3.OperationalError:  # нет такой таблицы
            pass
        cur.execute('''CREATE TABLE games (
            id INTEGER PRIMARY KEY ASC AUTOINCREMENT UNIQUE NOT NULL,
            title STRING)''')

        cur.execute('''INSERT INTO games (title, id)
            VALUES ('Binary game', 1)''')

        cur.execute('''CREATE TABLE records (
            id       INTEGER PRIMARY KEY ASC AUTOINCREMENT
                             UNIQUE
                             NOT NULL,
            game     INTEGER REFERENCES games (id),
            nickname STRING,
            score    INTEGER)''')
        self.con.commit()


class GamesTable(QMainWindow, Ui_RecordTable):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None, db: Database = None):
        super().__init__(parent)
        self.setupUi(self)
        self.horizontalLayout.deleteLater()  # ui для добавления рекорда
        self.lineEdit.deleteLater()
        self.pushButton.deleteLater()
        self.setWindowTitle('Таблица игр')

        if db is None:
            self.db = Database()
        else:
            self.db = db
        add_tables_menu(self, self.db)

        self.qdb = QtSql.QSqlDatabase('QSQLITE')
        self.qdb.setDatabaseName(self.db.db_file)
        self.qdb.open()

        self.model = QtSql.QSqlTableModel(self, self.qdb)
        self.refresh_view()

    def refresh_view(self):
        self.model.setQuery(self.qdb.exec('''SELECT
        title AS 'Название игры',
        id AS 'Номер игры'
        FROM games'''))
        self.tableView.setModel(self.model)

    def closeEvent(self, event):
        self.closed.emit()


class RecordTable(QMainWindow, Ui_RecordTable):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None, db: Database = None, score=None, game=None):
        super().__init__(parent)
        self.setupUi(self)

        if db is None:
            self.db = Database()
        else:
            self.db = db
        add_tables_menu(self, self.db)

        self.qdb = QtSql.QSqlDatabase('QSQLITE')
        self.qdb.setDatabaseName(self.db.db_file)
        self.qdb.open()

        self.model = QtSql.QSqlTableModel(self, self.qdb)
        self.refresh_view()

        if score is None or game is None:
            self.score = None
            self.game = None
            self.disable_adding()
        else:
            self.score = score
            self.game = game
            self.pushButton.clicked.connect(self.add_record)

    def add_record(self):
        nickname = self.lineEdit.text()
        if not nickname.strip():
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle('Введите имя')
            msgbox.setText('Введите имя')
            msgbox.show()
        else:
            cur = self.db.con.cursor()
            id_score = cur.execute(f'''SELECT id, score FROM records
            WHERE game = {self.game} AND nickname = '{nickname}' ''').fetchone()
            print(id_score)
            if id_score:
                id_, old_score = id_score
                if self.score > old_score:
                    cur.execute(f'''REPLACE INTO records (id, game, score, nickname) 
                                    VALUES ({id_}, {self.game}, {self.score}, '{nickname}')''')
            else:
                cur.execute(f'''INSERT INTO records (game, score, nickname) 
                VALUES ({self.game}, {self.score}, '{nickname}')''')
            self.db.con.commit()
            self.refresh_view()
            self.disable_adding()

    def disable_adding(self):
        self.lineEdit.setText('')
        self.lineEdit.setReadOnly(True)
        self.pushButton.setDisabled(True)

    def refresh_view(self):
        self.model.setQuery(self.qdb.exec('''SELECT
        nickname AS 'Никнейм',
        score AS 'Лучший счет',
        game AS 'Номер игры'
        FROM records
        ORDER BY score DESC, game ASC, nickname ASC'''))
        self.tableView.setModel(self.model)

    def closeEvent(self, event):
        self.closed.emit()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = RecordTable(score=124, game=1)
    ex.show()
    sys.exit(app.exec())
