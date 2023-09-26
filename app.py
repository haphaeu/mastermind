# -*- coding: utf-8 -*-
"""

Created on Jul 28 2021

@author: rarossi

"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtTest

import copy
import time
import itertools

import mastermind2 as mm

PEGS = "orgbcmyo"
RESP = "owko"


class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.mousePressEvent = self.mouse_clicked
        self.setWindowTitle("Mastermind")
        self.setMinimumSize(200, 400)
        self.reset()
        self.show()

    def reset(self):
        self.active_row = 0
        self.count = 0

        self.code = "cymb"

        self.guesses = [list("oooo") for _ in range(12)]
        self.responses = [list("oooo") for _ in range(12)]
        self.S = list(itertools.product(mm.PEGS, repeat=4))
        self.T = self.S[:]

    def play(self):
        self.count += 1
        guess = "".join(self.guesses[self.active_row])
        print(f"[{self.count}] {guess=} ", end="")
        resp = mm.get_response(guess, self.code)
        blacks, whites = resp
        print(f"-> {blacks=}, {whites=}")

        self.responses[self.active_row] = (
            "k" * blacks + "w" * whites + "o" * (4 - blacks - whites)
        )

        if blacks == 4:
            print(f"The code is {guess}/{self.code}.")
            self.active_row = -1
            return

        mm.prune(self.S, self.T, guess, resp, verbose=False)

        self.active_row += 1
        guess = self.guesses[self.active_row]
        guess[:] = mm.get_next_guess(self.S, self.T, verbose=False)

    def update_geometry(self):
        # ratio between h/w
        self.geom_ratio = 2
        # code pegs width ratio to w
        self.w1r = 0.8
        # response pegs witdh ratio to w
        self.w2r = 1.0 - self.w1r
        # pegs padding
        self.pegs_pad = 10
        # response padding
        self.resp_pad = 10
        # size of each square box with the pegs
        self.peg_box_size = int((self.w * self.w1r) / 4)
        # size of the pegs
        self.peg_size = int(self.peg_box_size - 2 * self.pegs_pad)
        # size of the box with responses
        self.response_box_size = int(self.w * self.w2r)
        # size of each reponse peg
        self.response_size = int((self.response_box_size - 4 * self.resp_pad) / 2)

        print(f"{self.peg_size=}, {self.response_size=}")

    def resizeEvent(self, event):
        print("resizeEvent() called")
        super().resizeEvent(event)
        self.w = self.size().width()  # window width
        self.h = self.size().height()  # window height
        self.update_geometry()

    def mouse_clicked(self, event):
        print("mouse_clicked() called")
        x = event.pos().x()
        y = event.pos().y()
        row = y // self.peg_box_size
        col = x // self.peg_box_size
        print(f"clicked round {row+1}, peg {col+1}")

        if not row == self.active_row or self.active_row == -1:
            return

        self.guesses[row][col] = PEGS[PEGS.find(self.guesses[row][col]) + 1]
        print(f"{''.join(self.guesses[row])}")
        self.update()

    def keyPressEvent(self, e):
        global board
        global board_hist
        if e.key() == QtCore.Qt.Key_R:
            print("Reset board.")
            self.reset()
            self.update()
        elif e.key() == QtCore.Qt.Key_P:
            if self.active_row == -1:
                print("game is over")
                return
            self.play()
            self.update()
        elif e.key() == QtCore.Qt.Key_A:
            self.solve_me()

    def paintEvent(self, e):
        print("paintEvent() called")
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        print("drawLines() called")

        pen = qp.pen()

        colors = {
            "o": QtCore.Qt.gray,
            "r": QtCore.Qt.red,
            "g": QtCore.Qt.green,
            "b": QtCore.Qt.blue,
            "c": QtCore.Qt.cyan,
            "y": QtCore.Qt.yellow,
            "m": QtCore.Qt.magenta,
        }
        responses_colors = {
            "o": QtCore.Qt.gray,
            "w": QtCore.Qt.white,
            "k": QtCore.Qt.black,
        }

        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtCore.Qt.gray)

        w = self.w
        h = self.h

        # background
        qp.fillRect(0, 0, w, h, QtCore.Qt.gray)

        # draw the board borders
        pen.setWidth(5)

        # draw the pegs
        for row in range(12):
            guess = self.guesses[row]
            response = self.responses[row]
            y = row * self.peg_box_size + self.pegs_pad
            for col in range(4):
                x = col * self.peg_box_size + self.pegs_pad
                s = self.peg_size
                qp.setBrush(colors[guess[col]])
                qp.drawEllipse(x, y, s, s)

            x = 4 * self.peg_box_size + self.pegs_pad
            i = 0
            for r in range(2):
                y1 = y + r * self.response_size + r * self.resp_pad
                for c in range(2):
                    x1 = x + c * self.response_size + c * self.resp_pad
                    s = self.response_size
                    qp.setBrush(responses_colors[response[i]])
                    qp.drawEllipse(x1, y1, s, s)
                    i += 1

        # qp.drawText(10, 20, "Score: %.1f%%" % score())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
