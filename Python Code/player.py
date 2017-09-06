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

    def __init__(self, player):
        super(RARemote, self).__init__()
        self.player = player
        self.serial = serial.Serial(SERIAL_PORT, SERIAL_BAUD_RATE)
    
    def run(self):

        while True:
            if not self.player.checkRunning():
                break
            msg = self.serial.readline()
            
            if msg == RARemote.PLAY_PAUSE:
                self.player.playPause()
            elif msg == RARemote.REWIND:
                self.player.rewind()
            elif msg == RARemote.FORWARD:
                self.player.forward()
            elif msg == RARemote.VOLUME_UP:
                self.player.volume_up()
            elif msg == RARemote.VOLUME_DOWN:
                self.player.volume_down()

class RAMP3PlayerRunner(Thread):

    def __init__(self, process):
        super(RAMP3PlayerRunner, self).__init__()
        self.process = process

    def run(self):
        self.process.wait()

class RAMP3Player(object):

    def __init__(self, filename):
        self.filename = filename
        self.playerProcess = None
        self.isPlaying = False
        self.__initPlayer()

    def rewind(self):
        if self.checkRunning():
            print "rewind"
            subprocess.Popen("echo -n $'\x1b\x5b\x44' > /tmp/mp3player", shell=True)

    def forward(self):
        if self.checkRunning():
            subprocess.Popen("echo -n $'\x1b\x5b\x43' > /tmp/mp3player", shell=True)

    def volume_up(self):
        if self.checkRunning:
            subprocess.Popen("echo -n + > /tmp/mp3player", shell=True)

    def volume_down(self):
        if self.checkRunning:
            subprocess.Popen("echo -n - > /tmp/mp3player", shell=True)

    def playPause(self):
        if self.checkRunning():
            if self.isPlaying:
                self.isPlaying = False
                subprocess.Popen("echo -n p >/tmp/mp3player", shell=True)
            else:
                subprocess.Popen("echo -n . >/tmp/mp3player", shell=True)
                self.isPlaying = True

    def __initPlayer(self):
        mkfifo = subprocess.Popen("mkfifo /tmp/mp3player", shell=True)
        mkfifo.wait()
        self.playerProcess = subprocess.Popen("omxplayer %s < /tmp/mp3player" % self.filename, shell=True)
        subprocess.Popen("echo -n . >/tmp/mp3player", shell=True) #start right away
        #self.isPlaying = True
        #runner = RAMP3PlayerRunner(self.playerProcess)
        #runner.start()
        remote = RARemote(self)
        remote.start()

        self.playerProcess.wait()

    def checkRunning(self):
        poll = self.playerProcess.poll()

        if poll is None:
            return True
        return False

if __name__ == "__main__":
    player = RAMP3Player("asin.mp3")
