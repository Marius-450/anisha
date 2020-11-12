# anisha
anisha is a CircuitPython lib to create displayio shapes behaving like neopixel objects that can be used with adafruit_led_animation.

## Version

Still alpha development version.

## General presentation

The idea is to animate shapes in a displayio environment, as if it was neopixel stripes. It permits to emulate as many strips you want and test animations without physically having to plug anything else. It can also of course be used to add some life in your programs, like a sparkling frame for a clock or a waiting animation during a request / reload ...
All the shapes are displayio tilegrids and can be moved, hidden, etc. You just have to add it to a group to display it.

# Arect

Arect is an animated rectangle shape class. 
3 animation modes are available : ` circular ` mode animates only the outline, `horizontal` and `vertical` modes animates the whole rectangle.

[Watch a demo on Youtube](https://www.youtube.com/watch?v=5NWonUOjqoQ)

# Apoly

Apoly is an animated polygon shape class. It is the base class for triangles, lines, broken lines etc, but it can also be used as-it.

# Aline

Aline is an animated line class. It is an "open polygon" with only 2 points.

# Atriangle

Atriangle is an animated triangle shape class.


