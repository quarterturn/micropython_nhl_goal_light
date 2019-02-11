"""
 NHL Goal Light

Checks the NHL stats website and turns on a light when a goal is detected. Meant for use with
something like a Sonoff 120V smart switch but any ESP8266 will do if it has enough flash
and RAM.

Uses wifimanager to provide a way for the user to configure the wireless. 

This version uses a Sonoff Basic to control a lamp using the relay.

"""

import wifimgr
import ntptime
import time
import machine
import urequests as requests
from lib import nhl
from lib import light

from machine import WDT

def sleep(sleep_period):
    """ Function to sleep if not in season or no game.
    Inputs sleep period depending if it's off season or no game."""
    # just sleep for 1 hour
    # let's try to avoid importing datetime
    time.sleep(3600)


def setup_nhl():
    # canes
    team_id = 12
    # st louis
    # team_id = 19
    # tbl
    # team_id = 14
    delay = get_nv_data("delay.txt")

    return (team_id, delay)

def get_nv_data(name):
    try:
        with open(name) as f:
            v = int(f.read())
    except OSError:
        v = 0
        try:
            with open(name, "w") as f:
               f.write(str(v))
        except OSError:
            print("Can't create file %s" % name)

    except ValueError:
        print("invalid data in file %s" % name)
        v = 0

    return v

def set_nv_data(name, value):
    try:
        with open(name, "w") as f:
            f.write(str(value))
    except OSError:
        print("Can't write to file %s" % name)

def callback(tim):
    state = machine.disable_irq()
    global delay
    global led
    led.value(0)
    time.sleep(0.01)
    if delay < 100:
	delay = delay + 10
        set_nv_data("delay.txt", delay)
    else:
        delay = 0
        set_nv_data("delay.txt", delay)
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        time.sleep(0.2)
        led.value(1)

    print("delay: ", delay)
    led.value(1)
    machine.enable_irq(state)

if __name__ == "__main__":

    # print("Connect or configure wireless")
    wlan = wifimgr.get_connection()
    if wlan is None:
        # print("Could not initialize the network connection.")
        while True:
            relay.value(1)
            time.sleep(1)
            relay.value(0)
            pass  # you shall not pass :D

    while not wlan.isconnected():
        # print(".", end="")
        time.sleep(1)
        
    # Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
    print("wireless ready, setting time")

    ntptime.settime()
    
    # setup pins
    # Sonoff LED seems to have a pullup
    led = machine.Pin(13, machine.Pin.OUT)
    relay = machine.Pin(12, machine.Pin.OUT)
    button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
    button.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)

    old_score = 0
    new_score = 0
    gameday = False
    season = False
    delay = 0

    light.setup()

    team_id, delay = setup_nhl()
    
    first_score_check = True

    wdt = WDT()  # enable it with a timeout of 5s
    print('Forcing WDT')
    wdt.feed()

    try:

        while (True):

            time.sleep(1)
            
            wdt.feed()

            # check if in season
            season = nhl.check_season()
            if season:
                # print("In season")
                # check game
                gameday = nhl.check_if_game(team_id)

                if gameday:
                    # print("Is gameday")
                    # light.game_today()
                    # check end of game
                    game_end = nhl.check_game_end(team_id)
                    led.value(0) 
                    
                    if not game_end:
                        # print("Game now")
                        # Check score online and save score
                        new_score = nhl.fetch_score(team_id)
                        
                        # if something went wrong getting the score
                        # set the score back to what it was
                        if new_score == -1:
                            new_score = old_score
 
                        print("Score: ", new_score)

                        # if the ESP8266 has rebooted
                        # prevent it from lighting the goal light
                        if first_score_check == True :
                            old_score = new_score
                            first_score_check = False

                        # If score change...
                        if new_score > old_score:
                            # save new score
                            # print("GOAL!")
                            # activate_goal_light()
                            # wait delay time
                            print("Score delay: ", delay)
                            time.sleep(delay)
                            light.activate_goal_light()
                            old_score = new_score

                    else:
                        # print("Game Over!")
                        old_score = 0 # Reset for new game
                        sleep("day")  # sleep till tomorrow
                        new_score = 0
                        led.value(1)
                else:
                    # print("No Game Today!")
                    sleep("day")  # sleep till tomorrow
                    new_score = 0
                    old_score = 0
                    led.value(1)
            else:
                # print("OFF SEASON!")
                sleep("season")  # sleep till next season
                new_score = 0
                old_score = 0
                led.value(1)

    except KeyboardInterrupt:
        print("\nCtrl-C pressed")
        light.cleanup()
        led.value(1)
