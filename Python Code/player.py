#!/usr/bin/env python
import subprocess
import serial
import time
from threading import Thread

SERIAL_PORT = "/dev/ttyACM0"
SERIAL_BAUD_RATE = 9600

class RARemote(Thread):

    PLAY_PAUSE = "FDA05F"
    OFF = "FD00FF"
    REWIND = "FD20DF"
    FORWARD = "FD609F"
    VOLUME_UP = "FD807F"
    VOLUME_DOWN = "FD906F"

    def __init__(self):
        super(RARemote, self).__init__()
        self.isPlaying = False
        self.serial = serial.Serial(SERIAL_PORT, SERIAL_BAUD_RATE)
    
    def run(self):

        while True:
            msg = self.serial.readline()
            if msg.strip() == RARemote.PLAY_PAUSE:
                print "Play/Pause"
                if self.isPlaying:
                    subprocess.Popen("echo -n p >/tmp/mp3player", shell=True)
                else:
                    subprocess.Popen("echo -n . >/tmp/mp3player", shell=True)
                    self.isPlaying = True
            elif msg.strip() == RARemote.REWIND:
                subprocess.Popen("echo -n $'\x1b\x5b\x44' > /tmp/mp3player", shell=True)
                print "Rewind"
            elif msg.strip() == RARemote.FORWARD:
                subprocess.Popen("echo -n $'\x1b\x5b\x43' > /tmp/mp3player", shell=True)
                print "Forward"
            elif msg.strip() == RARemote.VOLUME_UP:
                subprocess.Popen("echo -n + > /tmp/mp3player", shell=True)
                print "Volume Up"
            elif msg.strip() == RARemote.VOLUME_DOWN:
                subprocess.Popen("echo -n - > /tmp/mp3player", shell=True)
                print "Volume Down"

if __name__ == "__main__":
    remote = RARemote()
    remote.start()
