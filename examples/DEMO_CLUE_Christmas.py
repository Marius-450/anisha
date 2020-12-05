############
############
##
## Example of use of multiple animated shapes
## for boards with 240x240 buil-in display
## like the Clue or the M4sk
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

# Display setup

display = board.DISPLAY


arc1 = anisha.Aarc(200,2,200,60,29,colors=4,outline=0x606060, stroke=1, steps=None)


arc2 = anisha.Aarc(200,2,200,60,36,colors=4,outline=0x606060, stroke=1, steps=None)


tree = anisha.Apoly([(100,195), (100,175), (50,175), (80,140), (60,140), (90,105), (80,105), (119,60),
                (158,105), (148,105), (178,140), (158,140), (188,175), (138,175), (138,195)],
                colors=8,outline=0x006000, stroke=1, closed=True)


star1 = anisha.Astar(119,42,5,20,outline=GOLD,colors=16)


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

star_pulse = Pulse(star1, speed=0.05, period=6, color=GOLD)

tree_sparke = Sparkle(tree, speed=0.3, color=0x00FF00, num_sparkles=20)

lights_blink = Chase(lights, speed=1, size=1, spacing=2, color=0xFF0000)

animation_group = AnimationGroup(star_pulse, tree_sparke, lights_blink)


while True:
    animation_group.animate()

