import os
import tty
import sys
import termios
import atexit
import threading
import backend

from collections import defaultdict
from collections import deque

#Ensures that termios resets terminal settings any time the program exits
#os = original terminal settings stored at launch
def exit_handler(os):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, os)
    print("\nProgram Terminated!")

#UI class inhertits from thread so that program does
#not busy wait for UI
class UserInput(threading.Thread):
    def __init__(self, bkQueue, bkLock):
        #Get original terimal seting so they can be
        #reset at close
        self.orig_settings = termios.tcgetattr(sys.stdin)
        #Make sure terminal settings are reset before exiting
        atexit.register(exit_handler, self.orig_settings)
        #Last key pressed
        self.key = 0
        #current right speed (-100, 100)
        self.right = 0
        #current left speed (-100, 100)
        self.left = 0
        #most recent current from the arduino
        self.current = 0
        #angle of senor
        self.angle = 0
        #distance seen by sensor
        self.distance = 0
        #boolean whether sensor is turning
        self.turning = 0
        #Lock so that dataPrinting access is synchronized
        self.lock = threading.Lock()
        #Backend Queue Lock
        self.bkndLock = bkLock
        #Backend Queue reference
        self.bkndQueue = bkQueue


        threading.Thread.__init__(self)

    #Syncronized queue insertion
    def queueInsert(self):
        self.bkndLock.acquire()
        self.bkndQueue.append((self.left, self.right, self.turning))
        self.bkndLock.release()

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
        self.bkndLock.acquire()
        self.bkndQueue.append("q")
        self.bkndLock.release()
        self.running = False

    def invalid(self):
        pass

    def roam(self):
        self.turning = not self.turning

    def validate(self):
        if(self.left > 100):
            self.left = 100
        elif(self.left < -100):
            self.left = -100
        if(self.right > 100):
            self.right = 100
        elif(self.right < -100):
            self.right = -100

    #Syncronized Printing
    def printData(self):
        self.lock.acquire()
        #Reset terminal settings for printing
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_settings)
        os.system('clear')

        print("Pressed: ", self.key)
        print("------ Controls ------")
        print("w: Increment Speed (x10)")
        print("s: Decrement Speed (x10)")
        print("a: Turn Left")
        print("d: Turn Righ")
        print("e: Stop")
        print("q: Quit")
        print("R: Toggle Sensor Turing")
        print("")
        print("------- Status -------")
        print("Senor Turning(0/1): ", self.turning, "Left: ", self.left, " Right: ", self.right)
        
        print("Curent: ",self.current," Distance: ",self.distance," Angle: ",self.angle)
        #Set terminal back to raw mode so that single char is grabbed
        tty.setraw(sys.stdin)
        self.lock.release()

    def run(self):
        self.options = {'w': self.forward,
                        's': self.back,
                        'a': self.goLeft,
                        'd': self.goRight,
                        'q': self.quit,
                        'e': self.stop,
                        'r': self.roam}

        #Default value for a dict
        self.options = defaultdict(lambda: self.invalid, self.options)

        #Loop until input character is q
        while self.key != chr(113):  # q to exit
            self.printData()
            self.key = sys.stdin.read(1)[0]
            #call the function that maps to character pressed
            self.options[self.key]()
            self.validate()
            self.queueInsert()

        
