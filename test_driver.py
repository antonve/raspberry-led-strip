#!/usr/bin/env python

import time
import led_driver

print("LED strip driver test-drive")


commands = [
  ["Turn all LEDs off", led_driver.turn_off],
  ["Turn all LEDs white", led_driver.turn_all_white],
  ["Turn all LEDs red", led_driver.turn_all_red],
  ["Turn all LEDs blue", led_driver.turn_all_blue],
  ["Turn all LEDs green", led_driver.turn_all_green],
  ["Turn all LEDS to same random color", led_driver.turn_all_to_same_random],
]


for cmd in commands:
    print("-- " + cmd[0])
    cmd[1]()
    time.sleep(0.5)

