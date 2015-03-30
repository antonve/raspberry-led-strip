#!/usr/bin/env python

import random
import math
from time import sleep
import RPi.GPIO as GPIO

CLOCK_PIN = 22
DATA_PIN = 23
NUMBER_LEDS = 10

GPIO.setmode(GPIO.BCM)

GPIO.setup(CLOCK_PIN, GPIO.OUT)
GPIO.setup(DATA_PIN, GPIO.OUT)


def write_data(is_high):
    GPIO.output(CLOCK_PIN, False)
    GPIO.output(DATA_PIN, is_high)
    GPIO.output(CLOCK_PIN, True)

# byte = array of bits
def write_byte(byte_to_write):
    for bit in byte_to_write:
        write_data(bit)

def int_to_bit_array(color_int):
    color_int = color_int & 0xFF
    res = []
    for i in range(8):
        mask = int(math.pow(2, i))
        res.append(color_int & mask)
    return res

def write_rgb(red, green, blue):
    write_byte(int_to_bit_array(red))
    write_byte(int_to_bit_array(green))
    write_byte(int_to_bit_array(blue))

# colors: array with ten elements, each of which is an array with three values [red, green, blue]
def write_colors(colors):
    for color in colors:
        write_rgb(color[0], color[1], color[2])

