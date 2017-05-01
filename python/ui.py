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
    def __init__(self):#, backend):
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
        #reference to back end class
        #back end has queues for read/write to arduino
        self.bk = backend
        #If automated mode is true all user input accept r
        #with be ignored
        self.automated = False
        self.running = True
        #Lock so that dataPrinting access is synchronized
        self.lock = threading.Lock()
        
        threading.Thread.__init__(self)

    #Syncronized queue insertion
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
        self.running = False

    def invalid(self):
        pass

    def roam(self):
        self.stop()
        self.roam = True
        print("ROAMING");

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
        print("r: Roaming Mode")
        print("")
        print("------- Status -------")
        print("Left: ", self.left, " Right: ", self.right)
        
        #Check for indexing errors?
        data = self.getSenorData()
        
        #print("Curent: ",0," Senor Angle: ",0," Distance: ",0)
        print("Curent: ",data[0]," Distance: ",data[1]," Angle: ",data[2])
        
        #Set terminal back to raw mode so that single char is grabbed
        tty.setraw(sys.stdin)
        self.lock.release()

    def getSenorData(self):
        self.bk.rLock.acquire()
        data = self.bk.rx.popleft()
        self.bk.rLock.release()
        return data

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

        
