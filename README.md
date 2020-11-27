# anisha
<img src="https://raw.githubusercontent.com/Marius-450/screenshots/master/hearts.png" width="300" align="right">
anisha is a CircuitPython lib to create displayio shapes behaving like neopixel objects that can be used with adafruit_led_animation.

## Version

Still alpha development version.


## General presentation

The idea is to animate shapes in a displayio environment, as if it was neopixel stripes. It permits to emulate as many strips you want (limited by the memory available) and test animations without physically having to plug anything else. It can also of course be used to add some life in your programs, like a sparkling frame for a clock or a waiting animation during a request / reload ...
All the shapes are displayio tilegrids and can be moved, hidden, etc. You just have to add it to a group to display it.

## Credits

The base code for many shapes comes from adafruit_display_shapes https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes , except for the ellipse that was adapted from adafruit_circuitpython_turtle lib https://github.com/adafruit/Adafruit_CircuitPython_turtle .
I also shamelessly copied some code from pypixelbuf lib https://github.com/adafruit/Adafruit_CircuitPython_Pypixelbuf

Thanks to Adafruit for making this possible.


## Methods and attributes of Ashape objects

You can setup a new animation or animate the shape directly from your code without using led_animation :
* `shape.fill(color)` set all animated pixels of the shape to the color given in hex format, ex : `0xFF0000`
* `shape[pos] = color` set the pixels at `pos` to the color given in hex format, ex : `0xFF0000`, individually or using a slice.
* `shape._add_pixel(x,y,position=pos)` add x and y coordinates to the `shape._conversion_table` list. If `position` is ommited or greater than the pixel list length, it add a new point and increase `shape.n`. If `position` exists, it add the coordinates to this point. It checks for duplicates coordinages before adding it and return the position.
* `shape._line(x0,y0,x1,y1,color_index)` draw a line from x0,y0 to x1,y1 with the color_index, using `self.stroke`, and populate `shape._conversion_table` accordingly
* `shape._conversion_table` is a list of lists of coordinates. Each "pixel" can have multiple coordinates, wich permit lines with stroke > 1. It can be irregular, point 0 can have 10 coordinates while point 1 have only one.
* `shape.n` is the number of pixels (each one refering to one or many physical pixels of the display)

## shared parameters

* The number of colors in the `colors` parameter depends of the animations you plan to use. Blink only use 1 color at a time, while rainbow_* ones uses up to 256. More colors planned = more memory used. Logically, `shape.n` + 1 is a safe value. The code take care of recycling unused colors in the palette.
* `stroke` parameter sets the thickness of the lines drawn.
* `outline` is the color of the outine of the shape. Mandatory (but it may change in the future). 

# Classes
## Arect

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
    :param stroke: Thickness of the lines drawn, in pixels. Will not change the outer bound size set by ``width`` and
                   ``height``.
    :param anim_mode : "vertical", "horizontal" or "circular". default "circular"
    :param colors : Number of colors used in the bitmap and palette. default 128
```

## Apoly

Apoly is an animated polygon shape class. It is the base class for triangles, lines, broken lines etc, but it can also be used as-it.

```
polygon = anisha.Apoly(points, outline=None, colors=128, closed=True, stroke=1)

    :param points: A list of (x, y) tuples of the points
    :param outline: The outline of the polygon. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param closed : Boolean indicating if the shape is closed or not.
    :param stroke: Thickness of the lines drawn, in pixels
```


## Aline

Aline is an animated line class. It is an "open polygon" with only 2 points.

```
line = anisha.Aline(x0, y0, x1, y1, outline=None, colors=128, stroke=1)

    :param x0, y0: First point coordinates.
    :param x1, y1: Second point coordinates.    
    :param outline: The color of the line. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param stroke: Thickness of the lines drawn, in pixels
```

## Atriangle

Atriangle is an animated triangle shape class.

```
triangle = anisha.Atriangle(x0, y0, x1, y1, x2, y2, outline=None, colors=128, stroke=1)

    :param x0, y0: First point coordinates.
    :param x1, y1: Second point coordinates.
    :param x2, y2: Third point coordinates.
    :param outline: The outline of the triangle. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param stroke: Thickness of the lines drawn, in pixels
```
<img src="https://raw.githubusercontent.com/Marius-450/screenshots/master/Circle_arc_ellipse.png" width="300" align="right">

## Aellipse

Aellipse is an animated ellipse shape class. It can also be used to draw arcs and circles.  
It is a serie of `steps` lines, so it can also be a more or less regular polygon.  
If R == r, it draws a circle, or a circle arc.  

```
ellipse = anisha.Aellipse( x, y, R, r, start_angle = 0, end_angle = 360, angle_offset = 0, 
                          outline=None, colors=128, steps = None, stroke=1)

    :param x: x coordinate of the center of the ellipse.
    :param y: y coordinate of the center of the ellipse.
    :param R: Greatest radius in pixels.
    :param r: Smallest radius in pixels.
    :param start_angle: In degrees, clockwise. default = 0. 
    :param end_angle: In degrees. must be greater than start_angle. default = 360.
    :param angle_offset: Angle in degrees to rotate the shape counter-clockwise. default = 0 = start at East.
    :param outline: The outline of the ellipse. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps: Number of lines to draw. If None, computed to be roundish.
    :param stroke: Thickness of the lines drawn, in pixels
```


## Acircle

Acircle is an animated circle shape class.

```
circle = anisha.Acircle(x, y, radius, angle_offset=0, outline=None, colors=128, steps=None, stroke=1)

    :param x: x coordinate of the center of the circle
    :param y: y coordinate of the center of the circle
    :param radius: radius of the circle in pixels.
    :param angle_offset : angle in degrees where to start drawing and animating. 
    0 = East (default), 90 = North, 180 = West, 270 = South.
    :param outline: The outline of the circle. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps: Number of lines to draw. If None, computed to be roundish.
    :param stroke: Thickness of the lines drawn, in pixels
```

Under the hood, the circle is a regular polygon of `steps` sides. When `steps` is ommited (or set to `None`), the number of steps is computed automatically. Sometimes,  if the circle drawn is not perfectly round, you can ajust manually the `steps` parameter. Experiments shows only multiples of 4 draws symetric circles (but not always).

## Aregularpoly

Aregularpoly is an animated regular polygon shape class.

```
poly = anisha.Aregularpoly(x, y, sides, radius, angle_offset=0, outline=None, colors=128, stroke=1)

    :param x: x coordinate of the center of the polygon.
    :param y: y coordinate of the center of the polygon.
    :param sides: Number of sides of the polygon.
    :param radius: Radius in pixels.
    :param angle_offset : Angle in degrees to rotate the shape counter-clockwise. default = 0 = start at East.
    :param outline: The outline of the circle. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param stroke: Thickness of the lines drawn, in pixels
```


## Aegg

Aegg is an animated egg shape class.

```
egg = anisha.Aegg(x, y, sides, R, r, start_angle=0, end_angle=360, angle_offset=0, outline=None, colors=128, stroke=1)

    :param x: x coordinate of the center of the egg.
    :param y: y coordinate of the center of the egg.
    :param R: Greatest radius, in pixels.
    :param r: Smallest radius in pixels.
    :param start_angle: In degrees, clockwise. default = 0.
    :param end_angle: In degrees. must be greater than start_angle. default = 360.
    :param angle_offset : Angle in degrees to rotate the shape counter-clockwise. default = 0 = pointing North.
    :param outline: The outline of the egg. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param stroke: Thickness of the lines drawn, in pixels
```

## Aheart
Aheart is an animated heart shape class. The result is sometimes surprising. Using odd values for `height` parameter (that will also be the width) is more symetric. Approximative minimum height : 13. Below this, the shape is barely a heart. You can fine tune the steps to have better results than with computed one

```
heart = anisha.Aheart(x, y, height, start_angle=0, end_angle=360, angle_offset=0, outline=None, colors=128, steps=None, stroke=1)

    :param x: x coordinate of the center of the heart.
    :param y: y coordinate of the center of the heart.
    :param height: Height in pixels. will also be the width.
    :param start_angle: In degrees, clockwise. default = 0.
    :param end_angle: In degrees. must be greater than start_angle. default = 360.
    :param angle_offset : Angle in degrees to rotate the shape counter-clockwise. default = 0 = pointing South
    :param outline: The outline of the heart. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps:  Number of lines to draw. If None, computed to be roundish.
    :param stroke: Thickness of the lines drawn, in pixels
```

## Astar
Astar is an animated star shape class.
```
star = anisha.Aheart(x, y, points, radius, jump=2, angle_offset=0, outline=None, colors=128, stroke=1)

    :param x: x coordinate of the center of the star.
    :param y: y coordinate of the center of the star.
    :param points: Number of points to the star.
    :param radius: Radius of the circle in wich the star is inscribed. in pixels.
    :param jump: 
    :param angle_offset : Angle in degrees to rotate the star counter-clockwise. default = 0 = first point points toward North
    :param outline: The outline of the heart. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param stroke: Thickness of the lines drawn, in pixels
```

## Ashape
Ashape is the meta-class for animated shapes. Can be used as-it to draw a shape directly from code.py for example.

```
shape = anisha.Ashape(x, y, width, height, outline=None, colors=128, stroke=1)

    :param x: x coordinate of the upper left corner of the shape.
    :param y: y coordinate of the upper left corner of the shape.
    :param width: Width in pixels.
    :param height: Height in pixels.
    :param outline: The outline color of the shape. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param stroke: Thickness of the lines drawn, in pixels
```


## Schema

```
Ashape
    |
    |- Arect
    |
    |- Apoly
    |   |
    |   |- Atriangle
    |   |
    |   |- Aline
    |
    |- Aellipse
    |   |
    |   |- Acircle
    |   |   |
    |   |   |- Aregularpoly
    |   |
    |   |- Aegg
    |   |
    |   |- Aheart
    |   |
    |   |- Astar
    |
    |- Asinwave (coming soon)
```

# TODO

## More shapes

* just points
* arcs (already available via Aellipse)
* piechart (usefullness ?)
* sin wave (well ... x/y plotter, with the function in a helper method...) *work in progress*

## Bugs

* the stroke is out of the bitmap sometimes (more evident with Aline). 
*

## Improvements

* add an option to cut corners of a `shape._line()` at any angle (usefull with stars, polygons... ) 
* 
