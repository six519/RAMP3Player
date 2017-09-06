#!/usr/bin/env python
import subprocess
import serial
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

class RAMP3Player(object):

    def __init__(self):
        pass

if __name__ == "__main__":
    pass