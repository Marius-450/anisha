############
############
##
## Example of use of multiple animated shapes,
## proximity and color detection.
## For ADAFRUIT Clue boards
##
## CHRISTMAS DEMO
##
## By @Marius_450
##
##
############
############


# libs

import board
import displayio

import anisha

from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import GOLD
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.chase import Chase

import time
import busio
import digitalio
from adafruit_apds9960.apds9960 import APDS9960

# proximity sensor setup

i2c = busio.I2C(board.SCL, board.SDA)
apds = APDS9960(i2c, gain=0x02)

apds.enable_proximity = True

white_leds = digitalio.DigitalInOut(board.WHITE_LEDS)
white_leds.switch_to_output()

# Display setup

display = board.DISPLAY

# Moon shapes

arc1 = anisha.Aarc(200,2,200,60,29,colors=4,outline=0x606060, stroke=1, steps=None)


arc2 = anisha.Aarc(200,2,200,60,36,colors=4,outline=0x606060, stroke=1, steps=None)

# Christmas tree

tree = anisha.Apoly([(100,195), (100,175), (50,175), (80,140), (60,140), (90,105), (80,105), (119,60),
                (158,105), (148,105), (178,140), (158,140), (188,175), (138,175), (138,195)],
                colors=8,outline=0x006000, stroke=1, closed=True)

# Star

star1 = anisha.Astar(119,42,5,20,outline=GOLD,colors=16)

# Lights in the tree

lights = anisha.Apoints([(105,125), (100,170), (75, 180), (50,180), (80,135), (60,145), (95,100), (80,110), (119,85),
                (158,110), (143,100), (178,145), (158,135), (188,180), (163,180), (138,170), (133,125)],
                size=2, outline=0xFF0000,colors=4)


group = displayio.Group(max_size=5,scale=1)

group.append(arc1)
group.append(arc2)
group.append(tree)
group.append(star1)
group.append(lights)

display.show(group)

# Animations setup

star_pulse = Pulse(star1, speed=0.1, period=6, color=GOLD)

tree_sparkle = Sparkle(tree, speed=0.3, color=0x00FF00, num_sparkles=20)

lights_blink = Chase(lights, speed=1, size=1, spacing=2, color=0xFF0000)

animation_group = AnimationGroup(star_pulse, tree_sparkle, lights_blink)

# state variables

prox = False

while True:
    animation_group.animate()
    if prox is False and apds.proximity>15:
        # print("Proximity !")
        prox = True
        apds.enable_color = True
        white_leds.value = True
        while not apds.color_data_ready:
            time.sleep(0.005)
        # Take 5 readings in one second
        values = [[],[],[]]
        for i in range(5):
            r, g, b, c = apds.color_data
            d = r+ g+ b
            # print("r: {}, g: {}, b: {}, c: {}, d: {}".format(r, g, b, c, d))
            values[0].append(r//256)
            values[1].append(g//256)
            values[2].append(b//256)
            time.sleep(0.2)
        apds.enable_color = False
        white_leds.value = False
    if prox is True and apds.proximity<15:
        #print("No more proximity !")
        r, g, b = sum(values[0])//5, sum(values[1])//5, sum(values[2])//5
        # set the moon to the detected color
        arc1.fill((r,g,b))
        arc2.fill((r,g,b))

        prox = False

