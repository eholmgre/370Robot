#!/usr/bin/python3
import ui
import backend
import time


def main():

    bk = backend.Backend('/dev/ttyAMA0')
    bk.start()

    userInterface = ui.UserInput(bk)
    #userInterface = ui.UserInput()
    userInterface.start()

    while(userInterface.running):
        userInterface.printData()
        time.sleep(1)

    userInterface.join()
    backend.join()
    # ui terminates backend, so makes sense for it to join

if __name__ == '__main__':
    main()
