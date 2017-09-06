#!/usr/bin/env python
import subprocess
import serial
import time
from threading import Thread

class RARemote(object):

    PLAY_PAUSE = "FDA05F"
    OFF = "FD00FF"
    REWIND = "FD20DF"
    FORWARD = "FD609F"
    VOLUME_UP = "FD807F"
    VOLUME_DOWN = "FD906F"

    def __init__(self):
        pass

class RAMP3PlayerRunner(Thread):

    def __init__(self, process):
        super(RAMP3PlayerRunner, self).__init__()
        self.process = process

    def run(self):
        self.process.wait()

class RAMP3Player(object):

    def __init__(self, filename):
        self.filename = filename
        self.__initPlayer()
        self.playerProcess = None
        self.isPlaying = False

    def play(self):
        if self.checkRunning():
            if self.isPlaying:
                self.isPlaying = False
            else:
                self.isPlaying = True

    def __initPlayer(self):
        mkfifo = subprocess.Popen("mkfifo /tmp/mp3player", shell=True)
        mkfifo.wait()
        self.playerProcess = subprocess.Popen("omxplayer %s < /tmp/myp3player" % self.filename, shell=True)
        monitor = RAMP3PlayerRunner(self.playerProcess)
        monitor.start()
        self.play() #temporary

    def checkRunning(self):
        poll = self.playerProcess.poll()

        if poll is None:
            return True
        return False

if __name__ == "__main__":
    player = RAMP3Player("asin.mp3")
