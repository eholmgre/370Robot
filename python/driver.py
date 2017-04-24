#!/usr/bin/python3
#import backend
import ui
import time

def main():

 #   bk = backend.Backend('/dev/ttyAMA0')
  #  bk.start()

    #userInterface = ui.UserInput(bk)
    userInterface = ui.UserInput()
    userInterface.start()

    while(userInterface.running):
        userInterface.printData()
        time.sleep(1)
    

if __name__ == '__main__':
    main()
