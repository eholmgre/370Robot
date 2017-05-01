import threading
import serial
from collections import deque


class Backend(threading.Thread):

    class Receiver(threading.Thread):

        def __init__(self, connection, rDeque, rLock, runflag):
            self._con = connection
            self._queue = rDeque
            self._queueLock = rLock
            self.running = runflag
            threading.Thread.__init__(self)

        def run(self):
            while self.running:
                line = self._con.readline()
                self._queueLock.acquire()
                self._queue.append(line)
                self._queueLock.release()


    def __init__(self, device):
        self._con = serial.Serial(device, 9600)
        # receive queue: shared btwn Backend and Receiver, holds serial data from arduino
        self.rx = deque()
        self.rLock = threading.Lock()
        # transmit queue: shared btwn Frontend and Backend, holds commands to be sent to arduino
        self.tx = deque()
        self.tLock = threading.Lock()

        self._running = True
        self.receive = self.Receiver(self._con, self.rx, self.rLock, self._running)
        threading.Thread.__init__(self)

    def run(self):
        self.receive.start()
        while True:
            self.tLock.acquire()
            if self.tx:
                print(self.tx)
                cmd = self.tx.popleft()
                if cmd == "q":
                    self.tLock.release()
                    self.receive.running = False
                    self.receive.join()
                    break
                self._con.write(bytes("{} {}".format(cmd[0], cmd[1]), 'utf-8'))
            self.tLock.release()
