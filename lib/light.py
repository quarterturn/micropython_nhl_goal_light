import machine
import time


# using a Sonoff Basic
led = machine.Pin(13, machine.Pin.OUT)
relay = machine.Pin(12, machine.Pin.OUT)

def setup():
    # make sure LED is off
    led.value(1)
    # make sure relay is off
    relay.value(0)
    # light all LED briefly as a test
    led.value(0)
    time.sleep(0.5)
    led.value(1)

def activate_goal_light():
    # turn on relay 
    relay.value(1)
    # keep it on for 15 seconds
    time.sleep(15)
    # relay off
    relay.value(0)

def cleanup():
    led.value(1)
    relay.value(0)
