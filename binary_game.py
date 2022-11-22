from PyQt5 import QtCore, QtGui, QtWidgets
import random
from database import RecordTable


class BinaryGameRowWidget(QtWidgets.QWidget):
    solved = QtCore.pyqtSignal(int)

    def __init__(self, parent, target_value: int, score: int = None, digits: int = 8):
        QtWidgets.QWidget.__init__(self, parent)
        self.digits = digits
        self.setup_ui()

        self.target_label.setText(str(target_value))
        self.target_value = target_value

        self.result = 0
        self.result_label.setText(str(self.result))

        if score is not None:
            self.score = score
        else:
            self.score = 15 * bin(target_value)[2:].count('1')

    def setup_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.target_label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.target_label.sizePolicy().hasHeightForWidth())
        self.target_label.setSizePolicy(sizePolicy)
        self.target_label.setMinimumSize(QtCore.QSize(40, 40))
        self.target_label.setMaximumSize(QtCore.QSize(40, 40))
        self.target_label.setAlignment(QtCore.Qt.AlignCenter)
        self.target_label.setObjectName("target_label")
        self.horizontalLayout.addWidget(self.target_label)

        self.buttons = []
        for i in range(self.digits):
            btn = QtWidgets.QPushButton(self)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(btn.sizePolicy().hasHeightForWidth())
            # sizePolicy.setHeightForWidth(True)
            # sizePolicy.setWidthForHeight(True)
            btn.setSizePolicy(sizePolicy)
            btn.setMinimumSize(QtCore.QSize(40, 40))
            btn.setMaximumSize(QtCore.QSize(40, 40))
            btn.setObjectName(f"pushButton{i + 1}")
            btn.setText('0')
            self.horizontalLayout.addWidget(btn)
            self.buttons.append(btn)
            self._attach_btn_handler(btn, 2 ** (self.digits - i - 1))

        self.result_label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_label.sizePolicy().hasHeightForWidth())
        self.result_label.setSizePolicy(sizePolicy)
        self.result_label.setMinimumSize(QtCore.QSize(40, 40))
        self.result_label.setMaximumSize(QtCore.QSize(40, 40))
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setObjectName("result_label")
        self.horizontalLayout.addWidget(self.result_label)

        QtCore.QMetaObject.connectSlotsByName(self)

    def _check_correctness(self):
        if self.target_value == self.result:
            self.solved.emit(self.score)
            self.deleteLater()
            return True
        return False

    def _attach_btn_handler(self, btn: QtWidgets.QPushButton, value: int):
        def handler(self_):
            if btn.text() == '0':
                btn.setText('1')
                self.result += value
                self.result_label.setText(str(self.result))
            else:
                btn.setText('0')
                self.result -= value
                self.result_label.setText(str(self.result))
            self._check_correctness()
        btn.clicked.connect(handler)


class Ui_BinaryGame(object):
    def setupUi(self, MainWindow, digits=8):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(474, 360)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.level_label = QtWidgets.QLabel(self.centralwidget)
        self.level_label.setText('Уровень: ')
        self.horizontalLayout_3.addWidget(self.level_label)
        self.level_value_label = QtWidgets.QLabel(self.centralwidget)
        self.level_value_label.setText('1')
        self.horizontalLayout_3.addWidget(self.level_value_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_3.addWidget(self.label_13)
        self.score_value_label = QtWidgets.QLabel(self.centralwidget)
        self.score_value_label.setObjectName("label_14")
        self.horizontalLayout_3.addWidget(self.score_value_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setMinimumSize(QtCore.QSize(40, 0))
        self.label_11.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout.addWidget(self.label_11)
        for i in range(digits - 1, -1, -1):
            new_digit_label = QtWidgets.QLabel(self.centralwidget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(new_digit_label.sizePolicy().hasHeightForWidth())
            new_digit_label.setSizePolicy(sizePolicy)
            new_digit_label.setMinimumSize(QtCore.QSize(40, 0))
            new_digit_label.setMaximumSize(QtCore.QSize(40, 16777215))
            new_digit_label.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout.addWidget(new_digit_label)
            new_digit_label.setText(str(2**i))
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setMinimumSize(QtCore.QSize(40, 0))
        self.label_12.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.quit_action = QtWidgets.QAction(self.menubar)
        self.quit_action.setText('Выйти')
        self.menubar.addAction(self.quit_action)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Binary game"))
        self.label_13.setText(_translate("MainWindow", "Счёт: "))
        self.score_value_label.setText(_translate("MainWindow", "0"))


class BinaryGame(QtWidgets.QMainWindow, Ui_BinaryGame):
    closed = QtCore.pyqtSignal()
    game_id = 1
    max_rows = 5
    levels = {
        1: {'cooldown_s': 6, 'min_digits': 1, 'max_digits': 1, 'min_digit': 0, 'max_digit': 3, 'rows_until_next': 2},
        2: {'cooldown_s': 6, 'min_digits': 1, 'max_digits': 1, 'min_digit': 4, 'max_digit': 7, 'rows_until_next': 2},
        3: {'cooldown_s': 6, 'min_digits': 2, 'max_digits': 2, 'min_digit': 0, 'max_digit': 6, 'rows_until_next': 4},
        4: {'cooldown_s': 5, 'min_digits': 3, 'max_digits': 3, 'min_digit': 0, 'max_digit': 6, 'rows_until_next': 4},
        5: {'cooldown_s': 5, 'min_digits': 4, 'max_digits': 4, 'min_digit': 0, 'max_digit': 6, 'rows_until_next': 4},
        6: {'cooldown_s': 5, 'min_digits': 3, 'max_digits': 5, 'min_digit': 0, 'max_digit': 6, 'rows_until_next': 5},
        7: {'cooldown_s': 4, 'min_digits': 3, 'max_digits': 6, 'min_digit': 0, 'max_digit': 7, 'rows_until_next': 5},
        8: {'cooldown_s': 4, 'min_digits': 4, 'max_digits': 7, 'min_digit': 0, 'max_digit': 7, 'rows_until_next': 7}}
    default_level = {
        'cooldown_s': 3, 'min_digits': 1, 'max_digits': 8, 'min_digit': 0, 'max_digit': 7, 'rows_until_next': 7}
    digits = 8

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.setupUi(self, self.digits)
        self.quit_action.triggered.connect(self.close)
        self.db = db
        self.cooldown_s = 6
        self.timer = None
        self.reset_timer()
        self.score = 0
        self.level = 1
        self.rows_until_next = 2
        self.unsolved_rows = 0
        self.solved_in_level = 0
        self.spawn_new_row()

    def reset_timer(self):
        if self.timer is not None:
            self.killTimer(self.timer)
        self.timer = self.startTimer(self.cooldown_s * 1000)

    def spawn_new_row(self):
        if self.unsolved_rows + 1 > self.max_rows:
            self.close()

        level_data = self.levels.get(self.level, self.default_level)
        digits_amount = random.randint(level_data['min_digits'], level_data['max_digits'])
        digits = list(map((2).__pow__, range(level_data['min_digit'], level_data['max_digit'] + 1)))
        target_value = sum(random.sample(digits, k=digits_amount))
        score = self.level * 4 - level_data['min_digit'] * 2 + digits_amount * 3

        rw = BinaryGameRowWidget(self, target_value, score, self.digits)
        self.centralwidget.layout().insertWidget(2, rw)
        rw.solved.connect(self.solved)
        self.unsolved_rows += 1
        self.rows_until_next = level_data['rows_until_next']

    def timerEvent(self, event):
        self.spawn_new_row()

    def solved(self, score):
        self.score += score
        self.score_value_label.setText(str(self.score))
        self.unsolved_rows -= 1
        self.solved_in_level += 1
        if self.solved_in_level > self.rows_until_next:
            self.level += 1
            self.level_value_label.setText(str(self.level))
            self.solved_in_level = 0
        if self.unsolved_rows == 0:
            self.reset_timer()
            self.spawn_new_row()

    def closeEvent(self, event):
        text = f'Игра окончена\nСчёт: {self.score}'
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setWindowTitle(':(')
        msgbox.setText(text)
        self.hide()
        self.killTimer(self.timer)
        self.closed.emit()
        record_table = RecordTable(self, self.db, int(self.score_value_label.text()), self.game_id)
        record_table.show()
        msgbox.show()

    def keyPressEvent(self, e):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        screenshot.save('shot.png', 'png')
