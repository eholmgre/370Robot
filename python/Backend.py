import threading
import serial
from collections import deque


class Backend(threading.Thread):

    class Receiver(threading.Thread):

        def __init__(self, connection, rDeque, rLock):
            self._con = connection
            self._queue = rDeque
            self._queueLock = rLock
            threading.Thread.__init__(self)

        def run(self):
            while True:
                line = self._con.readline()
                self._queueLock.aquire()
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
        self.receive = self.Receiver(self._con, self.rx, self.rLock)
        threading.Thread.__init__(self)

    def run(self):
        self.receive.start()
        while True:
            self.rLock.aquire()
            if self.rx[-1] is not None:
                print(self.rx.pop())
            self.rLock.release()

            self.tLock.aquire()
            if self.tx[-1] is not None:
                cmd = self.tx.pop()
                if cmd == "q":
                    self.tLock.release
                    break
                self._con.write(b"{} {}".format(cmd[0], cmd[1]))
            self.tLock.release()
