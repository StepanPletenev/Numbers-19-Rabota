import pygame
pygame.init()
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle('Чиселки 19')
    w.showMaximized()
    sys.exit(app.exec_())\

    label = QLabel(w)
    label.setText("Приведствую тебя")
    label.move(100,300)
    label.show()

    btn = QPushButton
    btn.setText('Beheld')
    btn.move(110, 150)
    btn.show()
    btn.clicked.connect(dialog)
    w.show()
    w=pygame.display.set_mode(np.random.randint((7, 7)))
    w=np.random.randint(1,9,(7, 7))
    print(a)
    pygame.display.update()
    pygame.display.set_caption('Чиселки 19')
    game_over=False
while not game_over:
    for event in pygame.event.get():
        print(event)
        pygame.quit()
        quit()