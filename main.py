import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

class NumberGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Number19")
        self.setGeometry(100, 100, 600, 600)
        self.layout = QGridLayout()
        self.layout.setSpacing(5)

        self.lines = []
        self.selected_numbers = []

        for i in range(10):
            line = ""
            for _ in range(10):
                line += str(random.randint(1, 9))
            self.lines.append(list(line))

        for i in range(10):
            for j in range(10):
                btn = QPushButton(self)
                btn.setText(self.lines[i][j])
                btn.setStyleSheet("background-color: gray")
                btn.setFixedSize(50, 50)
                btn.clicked.connect(lambda _, x=i, y=j: self.number_clicked(x, y))
                self.layout.addWidget(btn, i, j)

        for i in range(10):
            self.layout.setColumnMinimumWidth(i, 50)
            self.layout.setRowMinimumHeight(i, 50)

        self.setLayout(self.layout)

    def number_clicked(self, x, y):
        if len(self.selected_numbers) == 2:
            self.remove_selected_numbers()
            return

        if (x, y) in self.selected_numbers:
            self.selected_numbers.remove((x, y))
        else:
            self.selected_numbers.append((x, y))

        self.update_buttons()

    def remove_selected_numbers(self):
        if len(self.selected_numbers) == 2:
            x1, y1 = self.selected_numbers[0]
            x2, y2 = self.selected_numbers[1]
            if self.can_remove(x1, y1, x2, y2):
                self.remove_numbers(x1, y1, x2, y2)
            self.selected_numbers = []
            self.update_buttons()

    def can_remove(self, x1, y1, x2, y2):
        if (0 <= x1 < len(self.lines) and 0 <= y1 < len(self.lines[0])
                and 0 <= x2 < len(self.lines) and 0 <= y2 < len(self.lines[0])):
            if self.lines[x1][y1] != " " and self.lines[x2][y2] != " ":
                num1 = int(self.lines[x1][y1])
                num2 = int(self.lines[x2][y2])
                if (num1 + num2 == 10 or num1 == num2) and (
                        (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)):
                    return True
        return False

    def remove_numbers(self, x1, y1, x2, y2):
        self.lines[x1][y1] = " "
        self.lines[x2][y2] = " "
        self.update_buttons()

        button1 = self.layout.itemAtPosition(x1, y1).widget()
        button2 = self.layout.itemAtPosition(x2, y2).widget()
        button1.setStyleSheet("background-color: gray")
        button1.setText(" ")
        button2.setStyleSheet("background-color: gray")
        button2.setText(" ")

    def update_buttons(self):
        for i in range(10):
            for j in range(10):
                button = self.layout.itemAtPosition(i, j).widget()
                if self.lines[i][j] != " ":
                    button.setText(self.lines[i][j])
                if (i, j) in self.selected_numbers:
                    button.setStyleSheet("background-color: green")
                else:
                    button.setStyleSheet("background-color: gray")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = NumberGame()
    game.show()
    sys.exit(app.exec_())