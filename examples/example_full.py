############
############
##
## example of animated shape
##
## By Marius_450
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
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE


# Display setup

matrix = Matrix(bit_depth=5)
display = matrix.display

# 114 colors is the minimum value for all the rainbow animations. 128 use same memory.
rect1 = anisha.Arect(16, 1, 30, 30, outline=0x004000, stroke=2, colors=128)


group = displayio.Group()
group.append(rect1)

display.show(group)

blink = Blink(rect1, speed=0.5, color=JADE)
colorcycle = ColorCycle(rect1, speed=0.4, colors=[MAGENTA, ORANGE])
comet = Comet(rect1, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(rect1, speed=0.1, size=3, spacing=6, color=WHITE)
pulse = Pulse(rect1, speed=0.1, period=3, color=AMBER)
sparkle = Sparkle(rect1, speed=0.1, color=PURPLE, num_sparkles=10)
solid = Solid(rect1, color=JADE)
rainbow = Rainbow(rect1, speed=0.1, period=2)
sparkle_pulse = SparklePulse(rect1, speed=0.1, period=3, color=JADE)
rainbow_comet = RainbowComet(rect1, speed=0.1, tail_length=7, bounce=True)
rainbow_chase = RainbowChase(rect1, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(rect1, speed=0.1, num_sparkles=15)
custom_color_chase = CustomColorChase(
    rect1, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)

animations = AnimationSequence(
    comet,
    blink,
    rainbow_sparkle,
    chase,
    pulse,
    sparkle,
    rainbow,
    solid,
    rainbow_comet,
    sparkle_pulse,
    rainbow_chase,
    custom_color_chase,
    advance_interval=5,
    auto_clear=True,
)

while True:
    animations.animate()
