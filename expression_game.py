import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import random
from database import RecordTable


class ExpressionGameRowWidget(QtWidgets.QWidget):
    solved = QtCore.pyqtSignal(int)

    def __init__(self, parent, nesting: int = 0, score: int = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.nesting = nesting
        self.python_expr = random_expression(nesting)
        self.target_value = eval(self.python_expr)
        self.readable_expr = translate_expression(self.python_expr)

        self.setup_ui()

        if score is not None:
            self.score = score
        else:
            self.score = round(10 * (nesting + 2)**1.7)

    def setup_ui(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.expression_label = QtWidgets.QLabel(self)
        self.expression_label.setAlignment(QtCore.Qt.AlignRight)
        self.expression_label.setObjectName("target_label")
        self.expression_label.setText(self.readable_expr)
        font = self.expression_label.font()
        font.setPointSize(26)
        self.expression_label.setFont(font)
        self.horizontalLayout.addWidget(self.expression_label)

        for btn_text in '01':
            btn = QtWidgets.QPushButton(self)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(btn.sizePolicy().hasHeightForWidth())
            btn.setSizePolicy(sizePolicy)
            btn.setMinimumSize(QtCore.QSize(40, 40))
            btn.setMaximumSize(QtCore.QSize(40, 40))
            btn.setObjectName(f"pushButton{btn_text}")
            btn.setText(btn_text)
            self.horizontalLayout.addWidget(btn)
            self._attach_btn_handler(btn, int(btn_text) == self.target_value)

        QtCore.QMetaObject.connectSlotsByName(self)

    def _check_correctness(self):
        if self.target_value == self.result:
            self.solved.emit(self.score)
            self.deleteLater()
            return True
        return False

    def _attach_btn_handler(self, btn: QtWidgets.QPushButton, right: bool):
        def handler(self_):
            if right:
                self.solved.emit(self.score)
            else:
                self.solved.emit(-self.score)
            self.deleteLater()
        btn.clicked.connect(handler)


class Ui_ExpressionGame(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 360)
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
        MainWindow.setWindowTitle("Expression game")
        self.label_13.setText("Счёт: ")
        self.score_value_label.setText("0")


class ExpressionGame(QtWidgets.QMainWindow, Ui_ExpressionGame):
    closed = QtCore.pyqtSignal()
    game_id = 2
    max_rows = 5
    levels = {
        1: {'cooldown_s': 5, 'min_nesting': 0, 'max_nesting': 0, 'rows_until_next': 4},
        2: {'cooldown_s': 10, 'min_nesting': 1, 'max_nesting': 1, 'rows_until_next': 6},
        3: {'cooldown_s': 20, 'min_nesting': 2, 'max_nesting': 2, 'rows_until_next': 6}}
    default_level = {
        'cooldown_s': 16, 'min_nesting': 0, 'max_nesting': 2, 'rows_until_next': 6}

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.setupUi(self)
        self.quit_action.triggered.connect(self.close)
        self.db = db
        self.cooldown_s = self.levels[1]['cooldown_s']
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
        nesting = random.randint(level_data['min_nesting'], level_data['max_nesting'])
        score = self.level * 3 + round(9 * (nesting + 2) ** 1.7)

        rw = ExpressionGameRowWidget(self, nesting, score)
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


def translate_expression(expr: str):
    new_expr = expr
    for python_op, new_op in zip(('and', 'or', '^', '<=', '==', 'not'), ('∧', '∨', '⊕', '→', '≡', '¬')):
        new_expr = new_expr.replace(python_op, new_op)
    return new_expr


def random_expression(nesting=0):
    if nesting == 0:
        d1, d2 = random.randint(0, 1), random.randint(0, 1)
    elif nesting == 1:
        d1, d2 = random.sample([random.randint(0, 1), '(' + random_expression(0) + ')'], k=2)
    else:
        n1, n2 = nesting % 2 + nesting // 2, (nesting - 1) % 2 + (nesting - 1) // 2
        d1 = '(' + random_expression(n1) + ')'
        d2 = '(' + random_expression(n2) + ')'
    op = random.choice(('and', 'or', '^', '<=', '==', 'not'))
    if op == 'not':
        return f'{op} {d1}'
    return f'{d1} {op} {d2}'


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ExpressionGame()
    ex.show()
    sys.exit(app.exec())
