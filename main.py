import sys
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QPushButton, QDesktopWidget, QLayout,
                             QLabel)


class MainMenu(QMainWindow):
    def start_game(self):
        self.hide()
        self.number_game = NumberGame()
        self.number_game.show()

    def __init__(self):
        super().__init__()

        self.number_game = None
        self.setWindowTitle("Number19")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #BF9730")
        self.setFixedSize(self.width(), self.height())

        game_title = QLabel("<h1>Добро пожаловать в головоломку Number 19</h1>", self)
        game_title.setGeometry(250, 200, 625, 100)

        start_button = QPushButton("Начать игру", self)
        start_button.setGeometry(300, 300, 400, 100)
        start_button.setStyleSheet("background-color: #A65900; font-size: 18px;")
        start_button.clicked.connect(self.start_game)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.close()


class NumberGame(QWidget):
    def __init__(self):
        super().__init__()
        self.timer_label = None
        self.lines = None
        self.layout = None
        self.selected_numbers = None
        self.time = None
        self.timer = None
        self.initUI()
        self.menu = MainMenu()
        self.win_message = None
        self.game_over = False

    def closeEvent(self, event):
        self.hide()
        self.menu.show()

    def initUI(self):
        self.setWindowTitle("Number19")
        self.setGeometry(100, 100, 1000, 800)
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.lines = []
        self.selected_numbers = []
        self.timer = QTimer()
        self.time = 0
        self.timer_label = None

        for i in range(10):
            line = ""
            for _ in range(10):
                line += str(random.randint(1, 9))
            self.lines.append(list(line))

        for i in range(10):
            for j in range(10):
                btn = QPushButton(self)
                btn.setText(self.lines[i][j])
                btn.setStyleSheet("background-color: #BF9730")
                button_size = 70
                btn.setFixedSize(button_size, button_size)
                btn.clicked.connect(lambda _, x=i, y=j: self.number_clicked(x, y))
                self.layout.addWidget(btn, i, j)

        timer_label_layout = QGridLayout()
        self.timer_label = QPushButton("00:00", self)
        self.timer_label.setFixedSize(150, 30)
        self.timer_label.setStyleSheet("background-color: #A65900; font-size: 20px;")
        timer_label_layout.addWidget(self.timer_label, 0, 0, 1, 1)
        self.layout.addLayout(timer_label_layout, 4, 10, 1, 1)

        exit_button = QPushButton("Выход", self)
        exit_button.setFixedSize(150, 30)
        exit_button.setStyleSheet("background-color: #A65900; font-size: 18px;")
        exit_button.clicked.connect(lambda _: self.close())
        self.layout.addWidget(exit_button, 5, 10, 1, 1)

        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start()

        self.setLayout(self.layout)
        self.move_center()

    def move_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def number_clicked(self, x, y):
        if self.game_over:
            return
        if len(self.selected_numbers) == 2:
            self.remove_selected_numbers()
            return

        if (x, y) in self.selected_numbers:
            self.selected_numbers.remove((x, y))
        elif self.lines[x][y] != " ":
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
                        (abs(x1 - x2) == 1 and y1 == y2) or
                        (abs(y1 - y2) == 1 and x1 == x2) or
                        (abs(x1 - x2) > 1 and y1 == y2 and all(
                            self.lines[i][y1] == " " for i in range(min(x1, x2) + 1, max(x1, x2)))) or
                        (abs(y1 - y2) > 1 and x1 == x2 and all(
                            self.lines[x1][i] == " " for i in range(min(y1, y2) + 1, max(y1, y2))))):
                    return True
        return False

    def remove_numbers(self, x1, y1, x2, y2):
        if x1 > x2 or (x1 == x2 and y1 > y2):
            x1, y1, x2, y2 = x2, y2, x1, y1
        self.lines[x1][y1] = " "
        self.lines[x2][y2] = " "

        for i in range(x1, 0, -1):
            self.lines[i][y1] = self.lines[i - 1][y1]
        self.lines[0][y1] = " "

        for i in range(x2, 0, -1):
            self.lines[i][y2] = self.lines[i - 1][y2]
        self.lines[0][y2] = " "

        self.update_buttons()

    def update_buttons(self):
        for i in range(10):
            for j in range(10):
                button = self.layout.itemAtPosition(i, j).widget()
                if self.lines[i][j] != " ":
                    button.setText(self.lines[i][j])
                    button.setStyleSheet("background-color: #BF9730")
                else:
                    button.setText("")
                    button.setFixedSize(0, 0)
                    button.setStyleSheet(
                        "background-color: white")
                if (i, j) in self.selected_numbers:
                    button.setStyleSheet("background-color: green")
                self.check_for_win()

    def update_timer(self):
        self.time += 1
        minutes = self.time // 60
        seconds = self.time % 60
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def check_for_win(self):
        for i in range(10):
            for j in range(10):
                if self.lines[i][j] != " ":
                    for x in range(10):
                        for y in range(10):
                            if self.can_remove(i, j, x, y):
                                return False
        self.timer.stop()
        win_label = QLabel("<h1>Игра окончена!</h1>", self)
        win_label.setGeometry(250, 200, 625, 100)
        self.layout.addWidget(win_label, 3, 0, 1, 10)
        self.game_over = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())
