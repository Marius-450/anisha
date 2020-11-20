############
############
##
## Example of use of animated polygons shapes
## With Matrixportal M4 and a 64x32 matrix (#adabox016)
##
## By @Marius_450
##
##
############
############


# libs


import board
import displayio
from adafruit_matrixportal.matrix import Matrix
import anisha


from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet

from adafruit_led_animation.sequence import AnimationSequence

from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE, YELLOW, RED, BLUE



# Display setup
# Use display = board.DISPLAY to use this code with a built-in display.

matrix = Matrix(bit_depth=5)
display = matrix.display

# delay in secs
d = 7

# number of colors
c = 128

poly1 = anisha.Apoly([(0, 0), (7, 31), (15, 2), (23, 31), (31,2), (39,31), (47, 2), (55, 31), (63,0)],outline=0xFF0000,colors=c)

group = displayio.Group(max_size=4)
group.append(poly1)

display.show(group)

blink = Blink(poly1, speed=0.5, color=0x00FF00)
comet = Comet(poly1, speed=0.01, color=PURPLE, tail_length=10, bounce=True)

animations = AnimationSequence(
    comet,
    blink,
    advance_interval=d,
    auto_clear=True
)

while True:
    animations.animate()

