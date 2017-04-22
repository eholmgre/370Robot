#!/usr/bin/python3
import os
import tty
import sys
import termios
import atexit
import threading
from collections import defaultdict
from collections import deque

import backend


def exit_handler(os):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, os)
    print("\nProgram Terminated!")


def main():
    orig_settings = termios.tcgetattr(sys.stdin)
    atexit.register(exit_handler, orig_settings)

    bk = backend.Backend('/dev/ttyAMA0')
    bk.start()

    ui = UserInput(orig_settings, bk)
    ui.start()


class UserInput:
    def __init__(self, os, backend):
        self.key = 0
        self.right = 0
        self.left = 0
        self.orig_settings = os
        self.bk = backend

    def queueInsert(self):
        self.bk.tLock.acquire()
        self.bk.tx.append((self.left, self.right))
        self.bk.tLock.release()

    def forward(self):
        if (self.left != self.right):
            self.right = self.left = max(self.left, self.right)
        self.right += 10
        self.left += 10


    def back(self):
        if (self.left != self.right):
            self.right = self.left = min(self.left, self.right)
        self.right -= 10
        self.left -= 10


    def goLeft(self):
        self.left -= 10
        self.right += 10


    def goRight(self):
        self.right -= 10
        self.left += 10


    def stop(self):
        self.right = 0
        self.left = 0


    def quit(self):
        self.left = 0
        self.right = 0
        self.queueInsert()
        self.bk.tx.append("q")
        self.bk.join()

    def invalid(self):
        pass


    def validate(self):
        if self.left > 100:
            self.left = 100
        elif self.left < -100:
            self.left = -100

        if self.right > 100:
            self.right = 100
        elif self.right < -100:
            self.right = -100


    def printData(self, key):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_settings)
        os.system('clear')
        print("Pressed: ", key)

        print("------ Controls ------")
        print("w: Increment Speed (x10)")
        print("s: Decrement Speed (x10)")
        print("a: Turn Left")
        print("d: Turn Righ")
        print("e: Stop")
        print("q: Quit")
        print("")
        print("------- Status -------")
        print("Left: ", self.left, " Right: ", self.right)


    def start(self):
        self.printData(self.key)

        self.options = {'w': self.forward,
                        's': self.back,
                        'a': self.goLeft,
                        'd': self.goRight,
                        'q': self.quit,
                        'e': self.stop}

        self.options = defaultdict(lambda: self.invalid, self.options)

        tty.setraw(sys.stdin)

        while self.key != chr(113):  # q to exit
            self.printData(self.key)
            tty.setraw(sys.stdin)
            self.key = sys.stdin.read(1)[0]
            self.options[self.key]()
            self.validate()
            self.queueInsert()


if __name__ == '__main__':
    main()
