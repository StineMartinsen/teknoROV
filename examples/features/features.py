import os
import subprocess
from tkinter import RIGHT

import Pyro4

from edurov import WebMethod


import RPi.GPIO as GPIO

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT) #UO
GPIO.setup(5,GPIO.OUT) #DOWN
GPIO.setup(6,GPIO.OUT) #RIGTH
GPIO.setup(26,GPIO.OUT) #LEFT


def control_motors():
    """Will be started in parallel by the WebMethod class"""
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            while rov.run:
                if keys.state('K_UP'):
                    print('Forward')
                    UP = True
                else:
                    UP = False
                if keys.state('K_DOWN'):
                    print('Backward')
                    DOWN = True
                else:
                    DOWN = False
                if keys.state('K_RIGHT'):
                    print('Right')
                    RIGHT = True
                else:
                    RIGTH = False
                if keys.state('K_LEFT'):
                    print('left')
                    LEFT = True
                else:
                    LEFT = False

                GPIO.output(4,UP)
                GPIO.output(5,DOWN)
                GPIO.output(6,RIGTH)
                GPIO.output(26,LEFT)

# Create the WebMethod class
web_method = WebMethod(
    index_file=os.path.join(os.path.dirname(__file__), 'index.html'),
    runtime_functions=control_motors,
)
# Start serving the web page, blocks the program after this point
web_method.serve()
