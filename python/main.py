#!/usr/bin/python3
import ui
import backend
import time


def main():

    bk = backend.Backend('/dev/ttyAMA0')


    userInterface = ui.UserInput(bk.tx, bk.tLock)
    bk.UI = userInterface

    bk.start()
    userInterface.start()

    userInterface.join()
    bk.join()

if __name__ == '__main__':
    main()
