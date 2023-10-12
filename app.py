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

        # The game has 3 modes:
        #   "auto": computer is code breaker and keeper.
        #   "breaker": user tries to break the code. The computer gives feedback.
        #   "keeper": user is the code keeper. The computer tries to break the code.
        self.game_mode = "breaker"

        self.reset()
        self.show()
        self.help()

    def reset(self):
        self.active_row = 0
        self.count = 0

        self.code = "cymb"

        self.guesses = [list("rrgg")]
        self.guesses.extend([list("oooo") for _ in range(11)])
        self.responses = [list("oooo") for _ in range(12)]
        self.S = list(itertools.product(mm.PEGS, repeat=4))
        self.T = self.S[:]

    def help(self):
        msg = ('Mastermind \n\n'
               'Choose game mode by pressing:\n\n'
               ' A: auto - computer vs computer\n'
               ' B: breaker - you are the code braker.\n'
               ' K: keeper - you are the code keeper.\n\n'
               'Switch between colors by clicking the pegs.\n\n'
               'If you are the code breaker, click on the bigger pegs\n'
               'until all 4 have a set color.\n\n'
               'If you are the code keeper, click on the smaller pegs\n'
               'to give feedback on the code pegs.\n\n'
               ' Play the next round by pressing P\n\n'
               'To show this help, press H'
        )
        box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'Help', msg)
        box.exec()
        
    def play(self):
        if self.game_mode == "auto":
            self.computer_guess()
            resp = self.computer_response()
            if self.check_won(resp):
                return

        elif self.game_mode == "breaker":
            if not self.human_guess():
                print("Invalid guess. Try again.")
                return
            resp = self.computer_response()
            if self.check_won(resp):
                return

        elif self.game_mode == "keeper":
            resp = self.human_response()
            if not resp:
                print("Invalid response. Try again.")
                return
            if self.check_won(resp):
                return
            self.active_row += 1
            self.computer_guess()
            self.update()
            return

        self.active_row += 1
        self.update()

    def check_won(self, resp):
        blacks, whites = resp
        if blacks == 4:
            print(f"The code is {''.join(self.guesses[self.active_row])}/{self.code}.")
            self.active_row = -1
            return True
        return False

    def human_guess(self):
        """Validate a user input guess"""
        assert self.game_mode == "breaker"
        g = "".join(self.guesses[self.active_row])
        return len(g) == 4 and set(g).issubset(set(mm.PEGS))

    def computer_guess(self):
        assert self.game_mode in {"auto", "keeper"}

        if self.active_row == 0:
            return

        last_guess = "".join(self.guesses[self.active_row - 1])
        resp_str = self.responses[self.active_row - 1]
        resp = resp_str.count("k"), resp_str.count("w")
        mm.prune(self.S, self.T, last_guess, resp, verbose=False)

        # check if S is not empty
        if not self.S:
            print('WARNING: S has become empty.')
            self.active_row = -1
            return
        
        next_guess = self.guesses[self.active_row]
        next_guess[:] = mm.get_next_guess(self.S, self.T, verbose=False)

    def human_response(self):
        """Validate a user input response"""
        assert self.game_mode == "keeper"

        resp_str = self.responses[self.active_row]
        resp = resp_str.count("k"), resp_str.count("w")
        blacks, whites = resp
        if (
            0 <= blacks <= 4
            and 0 <= whites <= 4
            and whites + blacks <= 4
            and not (blacks == 3 and whites == 1)
        ):
            return blacks, whites
        return False

    def computer_response(self):
        assert self.game_mode in {"auto", "breaker"}

        guess = "".join(self.guesses[self.active_row])
        resp = mm.get_response(guess, self.code)
        blacks, whites = resp
        self.responses[self.active_row] = (
            "k" * blacks + "w" * whites + "o" * (4 - blacks - whites)
        )
        return blacks, whites

    def old_play_old(self):
        def validate_guess(g):
            """Validate a user input guess"""
            return len(g) == 4 and set(g).issubset(set(mm.PEGS))

        def validate_response(r):
            """Validate a user input response"""
            blacks, whites = r
            return (
                0 <= blacks <= 4
                and 0 <= whites <= 4
                and whites + blacks <= 4
                and not (blacks == 3 and whites == 1)
            )

        if self.game_mode in {"auto", "keeper"} and self.active_row == 0:
            self.guesses[self.active_row] = list("rrgg")
            if self.game_mode == "keeper":
                self.active_row += 1
                self.update()
                return

        guess = "".join(self.guesses[self.active_row])
        if not validate_guess(guess):
            print("Invalid guess. Try again.")
            return

        self.count += 1
        print(f"[{self.count}] {guess=} ", end="")

        if self.game_mode in {"auto", "breaker"}:
            resp = mm.get_response(guess, self.code)
            blacks, whites = resp
            self.responses[self.active_row] = (
                "k" * blacks + "w" * whites + "o" * (4 - blacks - whites)
            )
        else:  # self.game_mode == 'keeper':
            resp_str = self.responses[self.active_row]
            resp = resp_str.count("k"), resp_str.count("w")
            if not validate_response(resp):
                print("Invalid response. Try again.")
                return
            blacks, whites = resp

        print(f"-> {blacks=}, {whites=}")

        if blacks == 4:
            print(f"The code is {guess}/{self.code}.")
            self.active_row = -1
            return

        if self.game_mode in {"auto", "keeper"}:
            mm.prune(self.S, self.T, guess, resp, verbose=False)

        self.active_row += 1

        if self.game_mode in {"auto", "keeper"}:
            guess = self.guesses[self.active_row]
            guess[:] = mm.get_next_guess(self.S, self.T, verbose=False)

        self.update()

    def update_geometry(self):
        # ratio between h/w
        self.geom_ratio = 2
        # pegs padding
        self.pegs_pad = 10
        # response padding
        self.resp_pad = 5
        # size of each square box with the pegs
        self.box_size = self.w // 5
        # size of the pegs
        self.peg_size = self.box_size - 2 * self.pegs_pad
        # size of each reponse peg
        self.response_size = self.box_size // 2 - 2 * self.resp_pad
        #print(f"{self.peg_size=}, {self.response_size=}")

    def resizeEvent(self, event):
        #print("resizeEvent() called")
        super().resizeEvent(event)
        self.w = self.size().width()  # window width
        self.h = self.size().height()  # window height
        self.update_geometry()

    def mouse_clicked(self, event):
        #print("mouse_clicked() called")

        if self.game_mode == "auto":
            return

        x = event.pos().x()
        y = event.pos().y()
        row = y // self.box_size
        col = x // self.box_size

        if not row == self.active_row or self.active_row == -1:
            return

        if self.game_mode == "breaker" and col < 4:
            # switch between the colors
            #print(f"clicked round {row+1}, peg {col+1}")
            self.guesses[row][col] = PEGS[PEGS.find(self.guesses[row][col]) + 1]
            #print(f"{''.join(self.guesses[row])}")

        elif self.game_mode == "keeper" and col == 4:
            xi = x - 4 * self.box_size
            yi = y - self.active_row * self.box_size
            coli = xi // (self.box_size // 2)
            rowi = yi // (self.box_size // 2)
            idx = int(coli + 2 * rowi)
            #print(f"clicked response {row+1}, peg {idx+1}")
            self.responses[row][idx] = RESP[RESP.find(self.responses[row][idx]) + 1]

        self.update()

    def keyPressEvent(self, e):
        global board
        global board_hist
        if e.key() == QtCore.Qt.Key_R:
            print("Reset board.")
            self.reset()
        elif e.key() == QtCore.Qt.Key_P:
            if self.active_row == -1:
                print("game is over")
                return
            self.play()
        elif e.key() == QtCore.Qt.Key_A:
            self.game_mode = "auto"
        elif e.key() == QtCore.Qt.Key_K:
            self.game_mode = "keeper"
        elif e.key() == QtCore.Qt.Key_B:
            self.game_mode = "breaker"
        elif e.key() == QtCore.Qt.Key_H:
            self.help()
        self.update()

    def paintEvent(self, e):
        # print("paintEvent() called")
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        # print("drawLines() called")

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

        # active row
        y = self.active_row * self.box_size
        qp.fillRect(0, y, w, self.box_size, QtCore.Qt.white)
        
        # draw the board borders
        pen.setWidth(5)

        # draw the pegs and responsed
        for row in range(12):
            guess = self.guesses[row]
            response = self.responses[row]
            y = row * self.box_size + self.pegs_pad
            s = self.peg_size
            # draw the guesses pegs
            for col in range(4):
                x = col * self.box_size + self.pegs_pad    
                qp.setBrush(colors[guess[col]])
                qp.drawEllipse(x, y, s, s)

            x = 4 * self.box_size
            y = row * self.box_size
            s = self.response_size
            i = 0
            # draw the response pegs
            for r in range(2):
                y1 = y + r * self.box_size // 2 + self.resp_pad
                for c in range(2):
                    x1 = x + c * self.box_size // 2 + self.resp_pad   
                    qp.setBrush(responses_colors[response[i]])
                    qp.drawEllipse(x1, y1, s, s)
                    i += 1
                    
        qp.fillRect(0, h - 12, w, h, QtCore.Qt.white)
        if self.active_row >= 0:
            qp.drawText(10, h - 2, f"Game mode: {self.game_mode}")
        else:
            qp.drawText(10, h - 2, f"Game over. Press 'R' to reset.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
