# micropython_nhl_goal_light

*** THIS PROJECT IS DEPRECATED ***
*** I am having too many random issues with hangs not being caught by the WDT ***
*** A new C++ version will be up soon in a separate repo which should be much more reliable ***

NHL Goal Light capable of running on Micropython Networked Hardware

This is a fork of arim215/nhl_goal_light
Modifications have been made to allow it to work within the RAM/stack space limits of an ESP8266. Tested with an ESP-12.

Also makes use of tayfunulu/WiFiManager to allow the end-user to configure their WAP info.

Tested on a Seeed Sonoff Basic smart switch. This is an esp8266 with 1 MB flash meant to control AC line-powered devices. See instructions here for flashing the Sonoff with Micropython: https://medium.com/cloud4rpi/getting-micropython-on-a-sonoff-smart-switch-1df6c071720a

I hard-code the team ID and use the Sonoff pushbutton to add a delay if needed. Each button press adds 10 seconds of delay, up to 100 seconds, after which it wraps around to 0 and give the LED a double blink to let you know. Delay is stored in delay.txt in the flash filesystem, so once you set it, it will stick on future power-cycles.

An FTDI-based USB serial adapter barely provides enough current from its built-in 3.3V supply to flash the esp8266. I highly recommend making an outboard 3.3V supply with an LT1117 3.3V TO-92 package reulator, or look for a USB serial adapter with an separate 3.3V regulator.

Please note the code is a work in progress. I see a few hangs and WDT-caused reboots during a game. I don't think it is a memory issue but other than that I'm not sure what it is.
