############
############
##
## Example of use of multiple animated roundish shapes
## With Matrixportal M4 and a 64x32 matrix (#adabox016)
##
## By @Marius_450
##
##
############
############


# libs

import time

import board
import displayio
from adafruit_matrixportal.matrix import Matrix
import anisha


from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import PURPLE


# Display setup
# Use display = board.DISPLAY to use this code with a built-in display.

matrix = Matrix(bit_depth=5)
display = matrix.display

# delay in secs
d = 7

# number of colors
# unused, 128 colors is the default now.
c = 128


ellipse1 = anisha.Aellipse(15,15,15,10,angle_offset=45,outline=0x004000)
arc1 = anisha.Aellipse(46,15,15,15,start_angle=180, end_angle=360, angle_offset=0,outline=0xFF0000)
circle1 = anisha.Acircle(46, 18, 13, outline=0x0000FF, angle_offset=90)

group = displayio.Group(max_size=4)
group.append(ellipse1)
group.append(arc1)
group.append(circle1)


display.show(group)

blink1 = Blink(arc1, speed=0.3, color=0xFF0000)
blink2 = Blink(ellipse1, speed=0.7, color=0x004000)
blink3 = Blink(circle1, speed=0.5, color=0x0000FF)

comet1 = Comet(ellipse1, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
comet2 = Comet(arc1, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
comet3 = Comet(circle1, speed=0.01, color=PURPLE, tail_length=10, bounce=True)

animations = AnimationSequence(
    AnimationGroup(blink1, blink2, blink3),
    AnimationGroup(comet1, comet2, comet3),
    advance_interval=d,
    auto_clear=True
)

time.sleep(10)

while True:
    animations.animate()
