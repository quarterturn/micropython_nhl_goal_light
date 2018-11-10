import machine
import time
import neopixel

# tone down the colors
# WS2128 are just too bright to look at full-strength
# except red briefly for the goal
RED = (255, 0, 0)
GREEN = (0, 25, 0)
BLUE = (0, 0, 25)
WHITE = (25, 25, 25)
BLACK = (0, 0, 0)
YELLOW = (25, 25, 0)
CYAN = (0, 25, 25)


# test using blue LED on Huzzah board
# led = machine.Pin(2, machine.Pin.OUT)
# use 8 LED neopixel stick for testing
# data on pin 15
np = neopixel.NeoPixel(machine.Pin(15), 8)

def setup():
    """ Function to setup raspberry pi GPIO mode and warnings. PIN 7 OUT and PIN 11 IN """
    # make sure LED is off
    # there's a pull-up so cancel it with a logic HIGH
    # led.value(1)
    # light all LEDs white briefly as a test
    set_color(np, WHITE)
    time.sleep(2)
    set_color(np, BLACK)


def activate_goal_light(gpio_event_var=0):
    # turn on LED
    # led.value(0)
    set_color(np, RED)
    # keep it on for 15 seconds
    time.sleep(15)
    # LED off
    # led.value(1)
    set_color(np, BLACK)


def cleanup():
    # led.value(1)
    set_color(np, BLACK)

def set_color(np, mycolor=BLACK):
    n = np.n
    for i in range(n):
        np[i] = mycolor
    np.write()

def no_game():
    np[0] = RED
    np.write()

def game_today():
    np[0] = YELLOW
    np.write()

def game_now():
    np[0] = WHITE
    np.write()

def display_score(score=0):
    n = np.n
    if score <= n:
        for i in range(score):
            np[i] = GREEN
    else:
        for i in range(n):
            np[i] = GREEN
    np.write()

def blank():
    # Turn off all the pixels.
    np.fill((0,0,0))
    np.write()

