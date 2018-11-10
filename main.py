"""
 NHL Goal Light

Checks the NHL stats website and turns on a light when a goal is detected. Meant for use with
something like a Sonoff 120V smart switch but any ESP8266 will do if it has enough flash
and RAM.

Uses wifimanager to provide a way for the user to configure the wireless. 

This version uses a dotstar LED stick to light up for a goal and also show the team
score.

TO DO: provide a web interface for setting the team and delay. Right now I am using a
five-position DIP switch and a 10K pot fed with a 22K/10K voltage divider and wiper to
the ADC input.
"""

import wifimgr
import ntptime
import time
import machine
import urequests as requests
from lib import nhl
from lib import light
#import gc
#import micropython

def sleep(sleep_period):
    """ Function to sleep if not in season or no game.
    Inputs sleep period depending if it's off season or no game."""
    # just sleep for 1 hour
    # let's try to avoid importing datetime
    time.sleep(3600)


def setup_nhl():
    """ reads the dip switch inputs to get the team index """
    """ looks up the actual team ID using a tuple """

    index = 0
    team_id = ""
    delay = 0

    # setup pins
    bit1 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
    bit2 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
    bit3 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
    bit4 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
    bit5 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

    # ADC
    # ESP32 version
    #adc = machine.ADC(machine.Pin(34))
    # ESP8266 Huzzah version
    adc = machine.ADC(0)

    # add up the binary value
    # remember it is active-low
    if bit1.value() == 0:
        index = index + 1
    if bit2.value() == 0:
        index = index + 2
    if bit3.value() == 0:
        index = index + 4
    if bit4.value() == 0:
        index = index + 8
    if bit5.value() == 0:
        index = index + 16

    # convert the switch setting to the team
    # up to team 10 it is a 1:1 mapping
    if index < 11:
        team_id = index
    # there is no team 11, so add one
    elif index > 10 and index < 28:
        team_id = index + 1
    # fit the teams in the 50's by adding 23
    else:
        team_id = index + 23

    # prevent impossible settings
    if team_id > 54:
        team_id = 54
    if team_id < 1:
        team_id = 1
        
        
             
    # read delay setting
    # divide by 8 gives a max of about 2 minutes in seconds
    # this ought to be enough
    # and will reduce the effect of noise in the reading
    delay = adc.read() / 8

    # print("team_id: {0}, delay seconds: {1}".format(team_id, delay))
    
    return (team_id, delay)


if __name__ == "__main__":

    # print("Connect or configure wireless")
    wlan = wifimgr.get_connection()
    if wlan is None:
        # print("Could not initialize the network connection.")
        while True:
            time.sleep(1)
            pass  # you shall not pass :D

    while not wlan.isconnected():
        # print(".", end="")
        time.sleep(1)
        
    # Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
    print("wireless ready, setting time")

    ntptime.settime()
    
    old_score = 0
    new_score = 0
    gameday = False
    season = False

    light.setup()

    team_id, delay = setup_nhl()
    
    # ESP32 WROVER
    # adc = machine.ADC(machine.Pin(34))
    # ESP 8266 Huzzah
    adc = machine.ADC(0)

    first_score_check = 1

    # machine.WDT().deinit()

    try:

        while (True):

            time.sleep(1)

            #gc.collect()
            #esp.meminfo()
            #print('MEMINFO: ')
            #micropython.mem_info()
            #gc.collect()
            #print('ALLOCATED: ', gc.mem_alloc())
            #print('FREE: ', gc.mem_free())

            print(".", end="")

            # read the delay adjustment every loop
            # so it can be tweaked during a game
            # divde by 8 to reduce noise and give a 2 minute max range
            delay = adc.read() / 8
            
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
                    
                    if not game_end:
                        # print("Game now")
                        # Check score online and save score
                        new_score = nhl.fetch_score(team_id)

                        if new_score == 0:
                            light.game_now()
                        else:
                            light.display_score(new_score)

                        # if the ESP8266 has rebooted
                        # prevent it from lighting the goal light
                        if first_score_check:
                            old_score = new_score
                            first_score_check = 0

                        # If score change...
                        if new_score > old_score:
                            # save new score
                            # print("GOAL!")
                            # activate_goal_light()
                            light.activate_goal_light()
                            old_score = new_score

                            # if using WS2128 LEDs you can show the score
                            # remove for relay version
                            light.display_score(new_score)

                    else:
                        # print("Game Over!")
                        # turn off LEDs used for testing
                        light.blank()
                        old_score = 0 # Reset for new game
                        sleep("day")  # sleep till tomorrow
                        new_score = 0
                else:
                    # print("No Game Today!")
                    # light.no_game()
                    sleep("day")  # sleep till tomorrow
                    new_score = 0
                    old_score = 0
            else:
                # print("OFF SEASON!")
                # light.no_game()
                sleep("season")  # sleep till next season
                new_score = 0
                old_score = 0

    except KeyboardInterrupt:
        print("\nCtrl-C pressed")
        light.cleanup()
