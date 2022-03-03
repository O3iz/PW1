import RPi.GPIO as gpio
import time

in1 = 17
in2 = 22
in3 = 23
in4 = 24

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)

def forward(sec):
    init()
    gpio.output(in1, True)
    gpio.output(in2, False)
    gpio.output(in3, True) 
    gpio.output(in4, False)
    time.sleep(sec)
    gpio.cleanup()

def reverse(sec):
    init()
    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, False) 
    gpio.output(in4, True)
    time.sleep(sec)
    gpio.cleanup()

def right(sec):
    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, False) 
    gpio.output(in4, True)
    time.sleep(sec)
    gpio.cleanup()
    
 def left(sec):
    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, False) 
    gpio.output(in4, True)
    time.sleep(sec)
    gpio.cleanup()
print "forward"
forward(3)
print "reverse"
reverse(3)
print "left"
left(3)
print "right"
right(3)
