############
############
##
## Example of use of multiple animated shapes
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
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE, YELLOW, RED, BLUE



# Display setup
# Use display = board.DISPLAY to use this code with a built-in display.

matrix = Matrix(bit_depth=5)
display = matrix.display

# delay in secs
d = 4

# number of colors
c = 128


rect1 = anisha.Arect(0, 0, 20, 32, outline=0x00FF00, stroke=1, colors=c, anim_mode="circular")

rect2 = anisha.Arect(21, 0, 3, 32, outline=0x0000FF, stroke=1, colors=c, anim_mode="vertical")

rect3 = anisha.Arect(25, 0, 39, 4, outline=0xFF0000, stroke=1, colors=c, anim_mode="horizontal")

rect4 = anisha.Arect(25, 5, 39, 27, outline=0x004000, stroke=2, colors=c, anim_mode="circular")

group = displayio.Group(max_size=4)
group.append(rect1)
group.append(rect2)
group.append(rect3)
group.append(rect4)


display.show(group)


pixels = rect1

blink = Blink(pixels, speed=0.5, color=0x00FF00)
colorcycle = ColorCycle(pixels, speed=0.4, colors=[MAGENTA, YELLOW])
comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
#pulse = Pulse(pixels, speed=0.1, period=3, color=0x00FF00)
sparkle = Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
solid = Solid(pixels, color=0x00FF00)
#rainbow = Rainbow(pixels, speed=0.1, period=2)
sparkle_pulse = SparklePulse(pixels, speed=0.1, period=3, color=0x00FF00)
rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=3, spacing=2, step=8)
#rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
custom_color_chase = CustomColorChase(
    pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)



blink2 = Blink(rect2, speed=0.5, color=0x0000FF)
colorcycle2 = ColorCycle(rect2, speed=0.4, colors=[MAGENTA, BLUE])
comet2 = Comet(rect2, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase2 = Chase(rect2, speed=0.1, size=3, spacing=6, color=WHITE)
#pulse2 = Pulse(rect2, speed=0.1, period=3, color=0x0000FF)
sparkle2 = Sparkle(rect2, speed=0.1, color=PURPLE, num_sparkles=10)
solid2 = Solid(rect2, color=0x0000FF)
#rainbow2 = Rainbow(rect2, speed=0.1, period=2)
sparkle_pulse2 = SparklePulse(rect2, speed=0.1, period=3, color=0x0000FF)
rainbow_comet2 = RainbowComet(rect2, speed=0.1, tail_length=7, bounce=True)
rainbow_chase2 = RainbowChase(rect2, speed=0.1, size=3, spacing=2, step=8)
#rainbow_sparkle2 = RainbowSparkle(rect2, speed=0.1, num_sparkles=15)
custom_color_chase2 = CustomColorChase(
    rect2, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)


blink3 = Blink(rect3, speed=0.5, color=0xFF0000)
colorcycle3 = ColorCycle(rect3, speed=0.4, colors=[JADE, ORANGE])
comet3 = Comet(rect3, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase3 = Chase(rect3, speed=0.1, size=3, spacing=6, color=WHITE)
#pulse3 = Pulse(rect3, speed=0.1, period=3, color=0xFF0000)
sparkle3 = Sparkle(rect3, speed=0.1, color=PURPLE, num_sparkles=10)
solid3 = Solid(rect3, color=0xFF0000)
#rainbow3 = Rainbow(rect3, speed=0.1, period=2)
sparkle_pulse3 = SparklePulse(rect3, speed=0.1, period=3, color=0xFF0000)
rainbow_comet3 = RainbowComet(rect3, speed=0.1, tail_length=7, bounce=True)
rainbow_chase3 = RainbowChase(rect3, speed=0.1, size=3, spacing=2, step=8)
#rainbow_sparkle3 = RainbowSparkle(rect3, speed=0.1, num_sparkles=15)
custom_color_chase3 = CustomColorChase(
    rect3, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)

blink4 = Blink(rect4, speed=0.5, color=0x004000)
colorcycle4 = ColorCycle(rect4, speed=0.4, colors=[RED, BLUE])
comet4 = Comet(rect4, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase4 = Chase(rect4, speed=0.1, size=3, spacing=6, color=WHITE)
#pulse4 = Pulse(rect4, speed=0.1, period=3, color=0x00C000)
sparkle4 = Sparkle(rect4, speed=0.1, color=PURPLE, num_sparkles=10)
solid4 = Solid(rect4, color=0x004000)
#rainbow4 = Rainbow(rect4, speed=0.1, period=2)
sparkle_pulse4 = SparklePulse(rect4, speed=0.1, period=3, color=0x00C000)
rainbow_comet4 = RainbowComet(rect4, speed=0.1, tail_length=7, bounce=True)
rainbow_chase4 = RainbowChase(rect4, speed=0.1, size=3, spacing=2, step=8)
#rainbow_sparkle4 = RainbowSparkle(rect4, speed=0.1, num_sparkles=15)
custom_color_chase4 = CustomColorChase(
    rect4, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)


animations = AnimationSequence(
    AnimationGroup(comet, comet2, comet3, comet4),
    AnimationGroup(blink, blink2, blink3, blink4),
    AnimationGroup(colorcycle, colorcycle2, colorcycle3, colorcycle4),
    AnimationGroup(chase, chase2, chase3, chase4),
    AnimationGroup(sparkle, sparkle2, sparkle3, sparkle4),
    AnimationGroup(solid, solid2, solid3, solid4),
    AnimationGroup(rainbow_comet, rainbow_comet2, rainbow_comet3, rainbow_comet4),
    AnimationGroup(sparkle_pulse, sparkle_pulse2, sparkle_pulse3, sparkle_pulse4),
    AnimationGroup(rainbow_chase, rainbow_chase2, rainbow_chase3, rainbow_chase4),
    AnimationGroup(custom_color_chase, custom_color_chase2, custom_color_chase3, custom_color_chase4),
    advance_interval=d,
    auto_clear=True
)


while True:
    animations.animate()
