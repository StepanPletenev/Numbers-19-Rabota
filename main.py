import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


class NumberGame(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Number Game")
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
                self.layout.addWidget(btn, i, j)

        for i in range(10):
            self.layout.setColumnMinimumWidth(i, 50)
            self.layout.setRowMinimumHeight(i, 50)

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
                        (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)):
                    return True
        return False

    def remove_numbers(self, x1, y1, x2, y2):
        self.lines[x1][y1] = " "
        self.lines[x2][y2] = " "
        self.update_buttons()

        for _ in range(2):
            removed = False
            for i in range(10):
                for j in range(10):
                    if self.lines[i][j] == " ":
                        continue
                    if (i > 0 and self.can_remove(i, j, i - 1, j)) or \
                            (i < 9 and self.can_remove(i, j, i + 1, j)) or \
                            (j > 0 and self.can_remove(i, j, i, j - 1)) or \
                            (j < 9 and self.can_remove(i, j, i, j + 1)):
                        self.remove_numbers(i, j, i, j)
                        removed = True
            if not removed:
                break

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
