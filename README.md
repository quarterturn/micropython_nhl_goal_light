# micropython_nhl_goal_light
NHL Goal Light capable of running on Micropython Networked Hardware

This is a fork of arim215/nhl_goal_light
Modifications have been made to allow it to work within the RAM/stack space limits of an ESP8266. Tested with an ESP-12.

Also makes use of tayfunulu/WiFiManager to allow the end-user to configure their WAP info.

This is a development version. It uses a dotstar 8 LED stick to indicate game in progress, score, and when a goal happens. I am using a pot on the ADC input to adjust the delay and a 5-position DIP switch to set the team ID. Non-dev version will target hardware like the Sonoff "smart switch" so a real 120V AC goal light can be used. This will require some mods to come up with a web interface to set delay and team ID.

Micropython and maybe urequests seem to have some bugs with regards to sometimes getting stuck on network stuff until the hardware watchdog kicks in and reboots it. I am working around this for now in code to prevent false goal inidication.
