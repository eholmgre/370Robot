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

    while(userInterface.running):
        userInterface.printData()
        time.sleep(1)

    userInterface.join()
    bk.join()
    # ui terminates backend, so makes sense for it to join

if __name__ == '__main__':
    main()
