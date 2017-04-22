import threading
import serial


class Backend(threading.Thread):
    class receive(threading.Thread):

        def __init__(connecion):
            # ohh whee
            self._con = connection

        def start():
            # get stuff
            while True:
                line = _con.readline();

    ## receive

    def __init__(device):
        self._con = serial.Serial(device, 9600)

    def start():
        # get mode from front

        if mode == m:
            manual()
        elif mode == ma:
            asistman()
        elif mode == a:
            auto();
        else:
            pass
            # retry mode from front

    def manual():

        while True:
            line = input()

            if line == 'f':
                con.write(b'50 50')
            elif line == 'ff':
                con.write(b'100 100')
            elif line == 'fs':
                con.write(b'10 10')
            elif line == 'fr':
                con.write(b'100 30')
            elif line == 'fl':
                con.write(b'30 100')
            elif line == 'b':
                con.write(b'-50 -50')
            elif line == 'bb':
                con.write(b'-100 -100')
            elif line == 'br':
                con.write(b'-100 -30')
            elif line == 'bl':
                con.write(b'-30 -100')
            elif line == 'bs':
                con.write(b'-10 -10')
            elif line == 'r':
                con.write(b'50 -50')
            elif line == 'rr':
                con.write(b'100 -100')
            elif line == 'rs':
                con.write(b'10 -10')
            elif line == 'l':
                con.write(b'-50 50')
            elif line == 'll':
                con.write(b'-100 100')
            elif line == 'ls':
                con.write(b'-10 10')
            elif line == 's':
                con.write(b'0 0')
            elif line == 'exit':
                con.write(b'0 0')
                continue
            else:
                print('unknown cmd')
                con.write(b'0 0')
                ## manual

## Backend
