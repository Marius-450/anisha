# anisha
anisha is a CircuitPython lib to create displayio shapes behaving like neopixel objects that can be used with adafruit_led_animation.

## Version

Still alpha development version.

## General presentation

The idea is to animate shapes in a displayio environment, as if it was neopixel stripes. It permits to emulate as many strips you want and test animations without physically having to plug anything else. It can also of course be used to add some life in your programs, like a sparkling frame for a clock or a waiting animation during a request / reload ...
All the shapes are displayio tilegrids and can be moved, hidden, etc. You just have to add it to a group to display it.

## Methods 

You can setup a new animation or animate the shape directly from your code without using led_animation :
* `shape.fill(color)` set all animated pixels of the shape to the color given in hex format, ex : `0xFF0000`
* `shape.__setitem__(pos, color)` set the pixels to the color given in hex format, ex : `0xFF0000`, individually or using a slice

## shared parameters

* The number of colors in the `colors` parameter depends of the animations you plan to use. Blink only use 1 color at a time, while rainbow_* ones uses 100+. More colors planned = more memory used.

# Arect

Arect is an animated rectangle shape class. 
3 animation modes are available : ` circular ` mode animates only the outline, `horizontal` and `vertical` modes animates the whole rectangle.

[Watch a demo on Youtube](https://www.youtube.com/watch?v=5NWonUOjqoQ)

```
rect = anisha.Arect(x, y,  width, height, fill=None, outline=None, stroke=1, anim_mode="circular", colors=128)
    
    :param x: The x-position of the top left corner.
    :param y: The y-position of the top left corner.
    :param width: The width of the rectangle.
    :param height: The height of the rectangle.
    :param fill: The color to fill the rectangle. Can be a hex value for a color or
                 ``None`` for transparent.
    :param outline: The outline of the rectangle. Must be a hex value for a color.
    :param stroke: Used for the outline. Will not change the outer bound size set by ``width`` and
                   ``height``.
    :param anim_mode : "vertical", "horizontal" or "circular". default "circular"
    :param colors : Number of colors used in the bitmap and palette. default 128
```

# Apoly

Apoly is an animated polygon shape class. It is the base class for triangles, lines, broken lines etc, but it can also be used as-it.

```
polygon = anisha.Apoly(points, outline=None, colors=128, closed=True)

    :param points: A list of (x, y) tuples of the points
    :param outline: The outline of the polygon. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param closed : Boolean indicating if the shape is closed or not.
```


# Aline

Aline is an animated line class. It is an "open polygon" with only 2 points.

```
line = anisha.Aline(x0, y0, x1, y1, outline=None, colors=128)

    :param x0, y0: First point coordinates.
    :param x1, y1: Second point coordinates.    
    :param outline: The color of the line. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
```

# Atriangle

Atriangle is an animated triangle shape class.

```
triangle = anisha.Atriangle(x0, y0, x1, y1, x2, y2, outline=None, colors=128)

    :param x0, y0: First point coordinates.
    :param x1, y1: Second point coordinates.
    :param x2, y2: Third point coordinates.
    :param outline: The outline of the triangle. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.

```

# Aellipse

Aellipse is an animated ellipse shape class. It can also be used to draw arcs and circles.  
It is a serie of `steps` lines, so it can also be a more or less regular polygon.  
If R == r, it draws a circle, or a circle arc.  

```
ellipse = anisha.Aellipse( x, y, R, r, start_angle = 0, end_angle = 360, angle_offset = 0, 
                          outline=None, colors=128, steps = None)

    :param x: x coordinate of the center of the ellipse.
    :param y: y coordinate of the center of the ellipse.
    :param R: greatest radius in pixels.
    :param r: smallest radius in pixels.
    :param start_angle: in degrees, clockwise. default = 0. 
    :param end_angle: in degrees. must be greater than start_angle. default = 360.
    :param angle_offset: angle in degrees to rotate the shape counter-clockwise. default = 0 = start at East.
    :param outline: The outline of the ellipse. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps: Number of lines to draw. If None, computed to be roundish.

```


# Acircle

Acircle is an animated circle shape class.

```
circle = anisha.Acircle(x, y, radius, angle_offset=0, outline=None, colors=128, steps=None)

    :param x: x coordinate of the center of the circle
    :param y: y coordinate of the center of the circle
    :param radius: radius of the circle in pixels.
    :param angle_offset : angle in degrees where to start drawing and animating. 
    0 = East (default), 90 = North, 180 = West, 270 = South.
    :param outline: The outline of the circle. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps: Number of lines to draw. If None, computed to be roundish.

```

Under the hood, the circle is a regular polygon of `steps` sides. When `steps` is ommited (or set to `None`), the number of steps is computed automatically. Sometimes,  if the circle drawn is not perfectly round, you can ajust manually the `steps`parameter. Experiments shows only multiples of 4 draws symetric circles (but not always).

# Aregularpoly

Aregularpoly is an animated regular polygon shape class.

```
poly = anisha.Aregularpoly(x, y, sides, radius, angle_offset=0, outline=None, colors=128)

    :param x: x coordinate of the center of the polygon.
    :param y: y coordinate of the center of the polygon.
    :param sides: number of sides of the polygon.
    :param radius: radius in pixels.
    :param angle_offset : angle in degrees to rotate the shape counter-clockwise. default = 0 = start at East.
    :param outline: The outline of the circle. Must be a hex value for a color.
    :param colors: Number of colors used in the bitmap and palette. default 128.
```
    def __init__(self, x, y, sides, radius, *, angle_offset=0, outline=None, colors=128):
