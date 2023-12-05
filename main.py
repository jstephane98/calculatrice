import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QSizePolicy, \
    QLayoutItem, QLabel


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Super Calculator V0.1")
        self.setWindowIcon(QIcon("icons/calculator-solid-24.png"))
        self.resize(500, 500)
        self.setStyleSheet("background: #333333; border: 10px solid #333333;")
        self.first_number = None
        self.operator = None
        self.comma_pressed = False
        self.egal_pressed = False
        self.memory = None
        self.setup_ui()
        self.setup_connection()

    def setup_ui(self):
        central_widget = QWidget()  # La classe de base de tous composants graphiques (c'est un conteneur)
        self.setCentralWidget(central_widget)

        grid = QGridLayout()  # l, c, h, w
        self.screen = QLabel("0")
        self.ce = QPushButton("CE")
        self.mc = QPushButton("MC")
        self.m_plus = QPushButton("M+")
        self.divide = QPushButton("/")

        self.btn_seven = QPushButton("7")
        self.btn_eight = QPushButton("8")
        self.btn_nine = QPushButton("9")
        self.multiplication = QPushButton("*")

        self.btn_four = QPushButton("4")
        self.btn_five = QPushButton("5")
        self.btn_six = QPushButton("6")
        self.minus = QPushButton("-")

        self.btn_one = QPushButton("1")
        self.btn_two = QPushButton("2")
        self.btn_three = QPushButton("3")
        self.plus = QPushButton("+")

        self.btn_zero = QPushButton("0")
        self.btn_comma = QPushButton(".")
        self.mr = QPushButton("MR")
        self.btn_egal = QPushButton("=")

        # Add Widget in grid
        grid.addWidget(self.screen, 0, 0, 1, 4)

        grid.addWidget(self.ce, 1, 0)
        grid.addWidget(self.mc, 1, 1)
        grid.addWidget(self.m_plus, 1, 2)
        grid.addWidget(self.divide, 1, 3)

        grid.addWidget(self.btn_seven, 2, 0)
        grid.addWidget(self.btn_eight, 2, 1)
        grid.addWidget(self.btn_nine, 2, 2)
        grid.addWidget(self.multiplication, 2, 3)

        grid.addWidget(self.btn_four, 3, 0)
        grid.addWidget(self.btn_five, 3, 1)
        grid.addWidget(self.btn_six, 3, 2)
        grid.addWidget(self.minus, 3, 3)

        grid.addWidget(self.btn_one, 4, 0)
        grid.addWidget(self.btn_two, 4, 1)
        grid.addWidget(self.btn_three, 4, 2)
        grid.addWidget(self.plus, 4, 3)

        grid.addWidget(self.btn_zero, 5, 0)
        grid.addWidget(self.btn_comma, 5, 1)
        grid.addWidget(self.mr, 5, 2)
        grid.addWidget(self.btn_egal, 5, 3)

        for line in range(6):
            grid.setRowStretch(line, 2 if line == 0 else 1)

        for idx in range(grid.count()):
            item: QLayoutItem = grid.itemAt(idx)
            widget = item.widget()
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if isinstance(widget, QPushButton):
                widget.setStyleSheet("background: #595959; color: white; font-weight: bold; font-size: 20px")
            else:
                widget.setStyleSheet("background: #a2af77; font-weight: bold")

        self.btn_egal.setStyleSheet("background: #f05a2D; font-weight: bold; font-size: 20px; color: white;")
        # equal_button.setObjectName("equal")

        central_widget.setLayout(grid)

    def setup_connection(self):
        self.btn_one.clicked.connect(self.write_to_screen)
        self.btn_two.clicked.connect(self.write_to_screen)
        self.btn_three.clicked.connect(self.write_to_screen)
        self.btn_four.clicked.connect(self.write_to_screen)
        self.btn_five.clicked.connect(self.write_to_screen)
        self.btn_six.clicked.connect(self.write_to_screen)
        self.btn_seven.clicked.connect(self.write_to_screen)
        self.btn_eight.clicked.connect(self.write_to_screen)
        self.btn_nine.clicked.connect(self.write_to_screen)
        self.btn_zero.clicked.connect(self.write_to_screen)
        self.btn_comma.clicked.connect(self.comma_press)

        # Opérator
        self.plus.clicked.connect(self.press_operator)
        self.minus.clicked.connect(self.press_operator)
        self.multiplication.clicked.connect(self.press_operator)
        self.divide.clicked.connect(self.press_operator)
        self.btn_egal.clicked.connect(self.execute)
        self.ce.clicked.connect(self.clear)

        # Memory
        self.m_plus.clicked.connect(self.add_memory)
        self.mc.clicked.connect(self.memory_clear)
        self.mr.clicked.connect(self.returned_memory)

    @Slot()
    def comma_press(self):
        self.comma_pressed = True

    @Slot()
    def write_to_screen(self):
        btn: QPushButton = self.sender()
        valueScreen = self.screen.text()

        if float(valueScreen) <= 0 or self.egal_pressed:
            showDisplay = btn.text()
        elif self.comma_pressed and valueScreen.isnumeric():
            showDisplay = f"{valueScreen}.{btn.text()}"
            self.comma_pressed = False
        else:
            showDisplay = f"{valueScreen}{btn.text()}"

        self.screen.setText(showDisplay)

    @Slot()
    def press_operator(self):
        operator: QPushButton = self.sender()
        self.first_number = float(self.screen.text())
        self.operator = operator.text()
        self.screen.setText("0")

    @Slot()
    def execute(self):
        resultValue = 0
        if self.operator == "+":
            resultValue = self.first_number + float(self.screen.text())
        elif self.operator == "-":
            resultValue = self.first_number - float(self.screen.text())
        elif self.operator == "/":
            resultValue = self.first_number / float(self.screen.text())
        elif self.operator == "*":
            resultValue = self.first_number * float(self.screen.text())

        self.egal_pressed = True
        self.screen.setText(str(resultValue))

    def clear(self):
        self.first_number = None
        self.screen.setText("0")
        self.operator = None
        self.comma_pressed = False
        self.egal_pressed = False

    def add_memory(self):
        self.memory = self.screen.text()

    def memory_clear(self):
        self.memory = None

    def returned_memory(self):
        self.screen.setText(self.memory)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWindow = MyWindow()
    myWindow.show()

    sys.exit(app.exec())
