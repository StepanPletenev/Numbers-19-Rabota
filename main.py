import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton


class NumberGame(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Number Game")
        self.setGeometry(100, 100, 600, 600)

        self.layout = QGridLayout()
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
                btn.clicked.connect(lambda checked, i=i, j=j: self.number_clicked(i, j))
                self.layout.addWidget(btn, i, j)

        self.setLayout(self.layout)

    def number_clicked(self, x, y):
        if (x, y) in self.selected_numbers:
            self.selected_numbers.remove((x, y))
        else:
            self.selected_numbers.append((x, y))

        if len(self.selected_numbers) == 2:
            x1, y1 = self.selected_numbers[0]
            x2, y2 = self.selected_numbers[1]
            if self.can_remove(x1, y1, x2, y2):
                self.remove_numbers(x1, y1, x2, y2)
                self.selected_numbers = []
            else:
                self.selected_numbers = []

        self.update_buttons()

    def can_remove(self, x1, y1, x2, y2):
        if (0 <= x1 < len(self.lines) and 0 <= y1 < len(self.lines[0])
                and 0 <= x2 < len(self.lines) and 0 <= y2 < len(self.lines[0])):
            if self.lines[x1][y1] != " " and self.lines[x2][y2] != " ":
                num1 = int(self.lines[x1][y1])
                num2 = int(self.lines[x2][y2])
                if (num1 + num2 == 10 or num1 == num2) and (
                        (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)):
                    return True
        return False

    def remove_numbers(self, x1, y1, x2, y2):
        self.lines[x1][y1] = " "
        self.lines[x2][y2] = " "

        for i in range(len(self.lines) - 1, 0, -1):
            for j in range(len(self.lines[i])):
                if self.lines[i][j] == " ":
                    for k in range(i - 1, -1, -1):
                        if self.lines[k][j] != " ":
                            self.lines[i][j] = self.lines[k][j]
                            self.lines[k][j] = " "
                            break

        self.update_buttons()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = NumberGame()
    game.show()
    sys.exit(app.exec_())
