#
# Animate Shapes
# by @marius-450
# based on adafruit_display_shapes / adafruit_led_animation  and trying to be
# compatible with matrixportal objects animations
#

import displayio
import math

import gc



class Ashape(displayio.TileGrid):
    def __init__(self, x, y, width, height, *, outline=None, colors=128, stroke=1):
        self.stroke=stroke
        self.height = height
        self.width = width
        self._palette = displayio.Palette(colors)
        self._palette.make_transparent(0)
        if outline is None:
            raise RuntimeError("base color must be provided for outline.")
        self._palette[1] = outline
        self._conversion_table = []
        self.n = 0
        self._bitmap = displayio.Bitmap(self.width, self.height, colors)
        super().__init__(self._bitmap, pixel_shader=self._palette, x=x, y=y)

    def show(self):
        pass
        #return self._transmit(self._post_brightness_buffer)

    def __len__(self):
        """
        Number of pixels.
        """
        return self.n

    def fill(self, color):
        """
        Fills the animated pixels with the given color.
        :param color: Color to set.
        """
        if color == 0x0 or color == (0,0,0):
            palette_index = 0
        elif color == self._palette[1]:
            palette_index = 1
        else:
            self._palette[2] = color
            palette_index = 2
        for index, points in enumerate(self._conversion_table):
            for p in points:
                x = p[0]
                y = p[1]
                self._bitmap[x,y] = palette_index

        for i in range(3,len(self._palette)):
            self._palette[i] = 0x000000


    def _set_item(
        self, index, r, g, b, w
    ):  # pylint: disable=too-many-locals,too-many-branches,too-many-arguments
        if index < 0:
            index += self.n
        if index >= self.n or index < 0:
            raise IndexError
        #is the color in the palette ?
        color = self._rgb2color(r,g,b)
        cindex = self._palette_index(color)
        if cindex == -1:
            # not in the palette.
            # is there a free slot for a new color ?
            cindex = self._palette_index(0,2)
            if cindex == -1:
                self._clean_palette()
                cindex = self._palette_index(0,2)
            if cindex == -1:
                raise RuntimeError("no more color available")
            self._palette[cindex] = color
        # set the pixels to the cindex value
        for x, y in self._conversion_table[index]:
            self._bitmap[x,y] = cindex


    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(self.n)
            for val_i, in_i in enumerate(range(start, stop, step)):
                r, g, b, w = self._parse_color(val[val_i])
                self._set_item(in_i, r, g, b, w)
        else:
            r, g, b, w = self._parse_color(val)
            self._set_item(index, r, g, b, w)


    def _parse_color(self, value):
        r = 0
        g = 0
        b = 0
        w = 0
        if isinstance(value, int):
            r = value >> 16
            g = (value >> 8) & 0xFF
            b = value & 0xFF
            w = 0
        else:
            if len(value) < 3 or len(value) > 4:
                raise ValueError(
                    "Expected tuple of length {}, got {}".format(3, len(value))
                )
            if len(value) == 3:
                r, g, b = value
            else:
                r, g, b, w = value

        return (r, g, b, w)


    def _rgb2color(self, r, g, b):
        color = r * 65536 + g * 256 + b
        return color

    def _palette_index(self, color, offset=0):
        # Return the first occurence of a color in self._palette, or -1
        for i in range(offset,len(self._palette)):
            if self._palette[i] == color:
                return i
        return -1

    def _getitem(self, index):
        r,g,b,w = self._parse_color( self._palette[self._bitmap[self._conversion_table[index][0]]])
        return (r,g,b)

    def __getitem__(self, index):
        if isinstance(index, slice):
            out = []
            for in_i in range( *index.indices(self.n) ):
                out.append(self._getitem(in_i))
            return out
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError
        return self._getitem(index)

    def _clean_palette(self):
        pixels = self[:]
        for i in range(2,len(self._palette)):
            r, g, b, w =  self._parse_color(self._palette[i])
            if (r,g,b) in pixels:
                continue
            self._palette[i] = 0x000000

    def _add_pixel(self,x,y,position=None):
        if position is None:
            position = len(self._conversion_table)
            if position > 0 and (x,y) in self._conversion_table[position - 1]:
                return position-1
            self._conversion_table.append([(x,y)])
            self.n = len(self._conversion_table)
            return position
        if len(self._conversion_table) > position and (x,y) in self._conversion_table[position]:
            return position
        if len(self._conversion_table) == position:
            self._conversion_table.append([(x,y)])
            self.n = len(self._conversion_table)
            return position
        self._conversion_table[position].append((x,y))
        return position

    # pylint: disable=invalid-name, too-many-locals, too-many-branches
    def _line(self, x0, y0, x1, y1, color):
        if self.stroke > 1:
            angle = math.degrees(math.atan2(y1-y0, x1-x0))
            angle = angle % 360
            angle = math.radians(angle)
        for ax, ay in self._compute_line(x0,y0,x1,y1):
            if self.stroke == 1:
                try:
                    self._bitmap[ax,ay] = color
                except IndexError:
                    print('indexerror : ',ax,ay)
                    continue
                self._add_pixel(ax,ay)
            else:
                bx = ax - math.sin(angle)*(self.stroke-1)
                by = ay + math.cos(angle)*(self.stroke-1)
                t = 0
                e = 0
                bx = int(round(bx))
                by = int(round(by))
                for tx,ty in self._compute_line(ax,ay,bx,by):
                    try: 
                        self._bitmap[tx,ty] = color
                    except IndexError:
                        print('indexerror : ',tx,ty)
                        t += 1
                        e += 1
                        continue
                    if t - e == 0:
                        pos = self._add_pixel(tx,ty)
                    else:
                        self._add_pixel(tx,ty,position=pos)
                    t += 1

    def _compute_line(self, x0, y0, x1, y1):
        if x0 == x1:
            step = 1
            if y0 > y1:
                step = -1
            for _h in range(y0, y1 + step,step):
                yield((x0, _h))
        elif y0 == y1:
            step = 1
            if x0 > x1:
                step = -1
            for _w in range(x0, x1 + step,step):
                yield((_w, y0))
        else:
            steep = abs(y1 - y0) > abs(x1 - x0)
            if steep:
                x0, y0 = y0, x0
                x1, y1 = y1, x1
            step = 1
            if x0 > x1:
                step = -1

            dx = abs(x1 - x0)
            dy = abs(y1 - y0)

            err = dx / 2

            if y0 > y1:
                ystep = 1
            else:
                ystep = -1
            for x in range(x0, x1 + step, step):
                if step > 0:
                    if steep:
                        yield((y0, x))
                    else:
                        yield((x, y0))
                    err = err - dy 
                    if err < 0:
                        y0 -= ystep
                        err += dx
                else:
                    if steep:
                        yield((y0,x))
                    else:
                        yield((x, y0))
                    err = err - dy
                    if err < 0:
                        y0 -= ystep
                        err += dx

class Arect(Ashape):
    """An animated rectangle.
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
    :param colors : Number of colors used in the bitmap and palette. default 128.
    """
    def __init__(self, x, y, width, height, *, fill=None, outline=None, stroke=1, anim_mode="circular", colors=128):
        super().__init__(x, y, width, height, outline=outline, stroke=stroke, colors=colors)
        
        self.anim_mode=anim_mode
        if fill is not None:
            self._palette[0] = fill
            self._palette.make_opaque(0)
        else:
            self._palette[0] = 0
            self._palette.make_transparent(0)

        if self.anim_mode == "circular":
            self.closed = True
            self._line(0,0,width-1,0,1)
            self._line(width-1,0,width-1,height-1,1)
            self._line(width-1,height-1,0,height-1,1)
            self._line(0,height-1,0,0,1)
        elif self.anim_mode == "horizontal":
            self.closed = False
            self.n = self.width
            self.stroke= self.height
            self._line(0,0,width-1,0,1)
            self.stroke=stroke
        elif self.anim_mode == "vertical":
            self.closed = False
            self.n = self.height
            self.stroke=self.width
            self._line(width-1,0,width-1,height-1,1)
            self.stroke=stroke
        else:
            print("Error : anime_mode '",self.anim_mode ,"' not recognised. use 'circular', 'horizontal' or 'vertical'")
            raise RuntimeError('anime mode not recognised')


        

class Apoly(Ashape):
    """An animated polygon.
    :param points: A list of (x, y) tuples of the points
    :param outline: The outline of the polygon. Must be a hex value for a color
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param closed : Boolean indicating if the shape is closed or not.
    """
    def __init__(self, points, *, outline=None, colors=128, closed=True,stroke=1):
        self.stroke=stroke
        xs = []
        ys = []
        self._conversion_table = []
        self.closed = closed

        for point in points:
            xs.append(point[0])
            ys.append(point[1])

        x_offset = min(xs)
        y_offset = min(ys)

        # Find the largest and smallest X values to figure out width for bitmap
        self.width = max(xs) - min(xs) + self.stroke
        self.height = max(ys) - min(ys) + self.stroke

        self._palette = displayio.Palette(colors)
        self._palette.make_transparent(0)
        self._bitmap = displayio.Bitmap(self.width, self.height, colors)

        if outline is not None:
            self.outline = outline
            self._palette[1] = outline
            for index, _ in enumerate(points):
                point_a = points[index]
                if index == len(points) - 1:
                    if self.closed:
                        point_b = points[0]
                    else:
                        break
                else:
                    point_b = points[index + 1]
                self._line(
                    point_a[0] - x_offset,
                    point_a[1] - y_offset,
                    point_b[0] - x_offset,
                    point_b[1] - y_offset,
                    1,)
            self.n = len(self._conversion_table)
        else:
            raise RuntimeError("base color must be provided for outline.")
        super(Ashape, self).__init__(
            self._bitmap, pixel_shader=self._palette, x=x_offset, y=y_offset
        )



class Atriangle(Apoly):
    """An animated triangle.
    :param x0, y0: First point coordinates
    :param x1, y1: Second point coordinates
    :param x2, y2: Third point coordinates
    :param outline: The outline of the triangle. Must be a hex value for a color
    :param colors: Number of colors used in the bitmap and palette. default 128.
    """
    def __init__(self, x0, y0, x1, y1, x2, y2, *, outline=None, colors=128, stroke=1):
        super().__init__([(x0, y0),(x1, y1),(x2, y2)], outline=outline, colors=colors, closed=True, stroke=stroke)



class Aline(Apoly):
    """An animated line.
    :param x0, y0: First point coordinates
    :param x1, y1: Second point coordinates
    :param outline: The color of the line. Must be a hex value for a color
    :param colors: Number of colors used in the bitmap and palette. default 128.
    """
    def __init__(self, x0, y0, x1, y1, *, outline=None, colors=128, stroke=1):
        super().__init__([(x0, y0),(x1, y1)], outline=outline, colors=colors, closed=False, stroke=stroke)

class Aellipse(Ashape):
    """An animated ellipse.
    :param x: x coordinate of the center of the ellipse.
    :param y: y coordinate of the center of the ellipse.
    :param R: greatest radius in pixels.
    :param r: smallest radius in pixels.
    :param start_angle: in degrees, clockwise. default = 0.
    :param end_angle: in degrees. must be greater than start_angle. default = 360.
    :param angle_offset: angle in degrees to rotate the shape clockwise. default = 0 = East.
    :param outline: The outline of the ellipse. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps: Number of lines to draw. If None, computed to be roundish.
    all angles can be negatives or greater than 360.
    """
    def __init__(self, x, y, R, r, *, start_angle = 0, end_angle = 360, angle_offset = 0, outline=None, colors=128, steps = None, stroke=1):
        gc.collect()
        self.stroke=stroke
        if end_angle - start_angle >= 360:
            self.closed = True
        else:
            self.closed = False

        self.width = R*2
        self.height = r*2
        self._palette = displayio.Palette(colors)
        self._palette.make_transparent(0)
        max_size = int(round(max(self.width, self.height)))
        # temporarily oversized
        self._bitmap = displayio.Bitmap(max_size, max_size, colors)

        xs = []
        ys = []

        self._conversion_table = []

        x_offset = x - (max_size-1)//2
        y_offset = y - (max_size-1)//2

        if outline is not None:
            if steps is None:
                mean = int((r + R)/2)
                if mean > 9:
                    frac = (end_angle - start_angle)/360
                    steps = int(min(3 + (mean+1) / 4.0, 12.0) * frac) * 4
                else:
                    if mean == 5:
                        steps = 20
                    elif mean == 6:
                        steps = 28
                    elif mean == 7:
                        steps = 44
                    elif mean == 8:
                        steps = 40
                    elif mean == 9:
                        steps = 44
                    else:
                        steps = 20
            step = 360 / steps
            theta = start_angle
            off_r = math.radians(angle_offset)
            self._palette[1] = outline
            while theta <= end_angle:
                ax , ay = self._curveplot(R, r, theta)
                if angle_offset != 0:
                    nx = ax * math.cos(off_r) + ay * math.sin(off_r)
                    ny = -ax * math.sin(off_r) + ay * math.cos(off_r)
                    ax = nx
                    ay = ny
                ax = int(round(ax + (max_size-1)/2,0))
                ay = int(round(ay + (max_size-1)/2,0))
                xs.append(ax)
                ys.append(ay)
                if len(xs) > 1:
                    self._line(xs[-2], ys[-2], ax, ay, 1)
                theta += step
        else:
            raise RuntimeError("base color must be provided for outline.")
        self.n = len(self._conversion_table)

        x_new_offset = min(xs)
        y_new_offset = min(ys)

        # Find the largest and smallest X and Y values to figure out width and height for the bitmap
        used_width = max(xs) - min(xs) + 1
        used_height = max(ys) - min(ys) + 1

        # Resize bitmap if needed.
        if used_width != max_size or used_height != max_size:
            new_bitmap = displayio.Bitmap(used_width, used_height, colors)
            for px in range(max_size):
                for py in range(max_size):
                    if self._bitmap[px,py] == 1:
                        new_bitmap[px - x_new_offset, py - y_new_offset] = 1
            for pos, points in enumerate(self._conversion_table):
                l = []
                for p in points:
                    l.append((p[0]-x_new_offset,p[1]-y_new_offset))
                self._conversion_table[pos] = l
            self._bitmap = new_bitmap
        gc.collect()
        super(Ashape, self).__init__(
            self._bitmap, pixel_shader=self._palette, x=x_offset+x_new_offset, y=y_offset+y_new_offset
        )
    def _curveplot(self, R, r, theta):
        #ellipse shape
        t = math.radians(theta)
        ax = math.cos(t) * (R-0.5)
        ay = math.sin(t) * (r-0.5)
        return (ax, ay)

class Acircle(Aellipse):
    """An animated circle.
    :param x: x coordinate of the center of the circle.
    :param y: y coordinate of the center of the circle.
    :param radius: radius of the circle in pixels.
    :param angle_offset : angle in degrees where to start drawing and animating.
    0 = East (default), 90 = North, 180 = West, 270 = South.
    :param outline: The outline of the circle. Must be a hex value for a color.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps: Number of lines to draw. If None, computed to be roundish.
    """
    def __init__(self, x, y, radius, *, angle_offset=0, outline=None, colors=128, steps=None, stroke=1):
        super().__init__(x, y, radius, radius, angle_offset=angle_offset, outline=outline, colors=colors, steps=steps, stroke=stroke)

class Aregularpoly(Acircle):
    """An animated regular polygon.
    :param x: x coordinate of the center of the polygon.
    :param y: y coordinate of the center of the polygon.
    :param sides: number of sides of the polygon.
    :param radius: radius in pixels.
    :param angle_offset : angle in degrees to rotate the shape counter-clockwise. default = 0 = start at East.
    :param outline: The outline of the circle. Must be a hex value for a color.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    """
    def __init__(self, x, y, sides, radius, *, angle_offset=0, outline=None, colors=128, stroke=1):
        super().__init__(x, y, radius, angle_offset=angle_offset+((360/sides)/2), outline=outline, colors=colors, steps=sides, stroke=stroke)

class Aegg(Aellipse):
    """An animated egg.
    :param x: x coordinate of the center of the egg.
    :param y: y coordinate of the center of the egg.
    :param R: greatest radius in pixels.
    :param r: smallest radius in pixels.
    :param start_angle: in degrees, clockwise. default = 0.
    :param end_angle: in degrees. must be greater than start_angle. default = 360.
    :param angle_offset: angle in degrees to rotate the shape clockwise. default = 0 = East.
    :param outline: The outline of the ellipse. Must be a hex value for a color or a 3 values tuple.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps: Number of lines to draw. If None, computed to be roundish.
    all angles can be negatives or greater than 360.
    """
    def __init__(self, x, y, R, r, *, start_angle = 0, end_angle = 360, angle_offset = 0, outline=None, colors=128, steps = None, stroke=1):
        super().__init__(x, y, R, r, angle_offset=angle_offset, start_angle = start_angle-180 , end_angle = end_angle-180,
                         outline=outline, colors=colors, steps=steps, stroke=stroke)

    def _curveplot(self, R, r, theta):
        #egg shape
        t = math.radians(theta)
        ax = -math.sin(t+math.sin(t)/4) * (r-0.5)
        ay = (R-0.5) * math.cos(t)
        return (ax, ay)

class Aheart(Aellipse):
    """An animated heart 
    :param x: x coordinate of the center of the heart.
    :param y: y coordinate of the center of the heart.
    :param height: height in pixels. will also be the width.
    :param start_angle: in degrees, clockwise. default = 0.
    :param end_angle: in degrees. must be greater than start_angle. default = 360.
    :param angle_offset : angle in degrees to rotate the shape counter-clockwise. default = 0 = pointing South
    :param outline: The outline of the heart. Must be a hex value for a color.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param steps:  Number of lines to draw. If None, computed to be roundish.
    """
    def __init__(self, x, y, height, *, start_angle = 0, end_angle = 360, angle_offset = 0, outline=None, colors=128, steps = None, stroke=1):
        super().__init__(x, y, (height/2)+1, height/2, angle_offset=angle_offset, start_angle = start_angle, end_angle = end_angle,
                         outline=outline, colors=colors, steps=steps, stroke=stroke)

    def _curveplot(self, R, r, theta):
        #heart shape
        t = math.radians(theta)
        t = (t - math.pi)
        ax = (r-0.5)*(math.sin(t)**3)
        ay = ((r-1.5)* 0.95 * math.cos(t)-((r-1.5)/2.8)*math.cos(2*t)-((r-1.5)/6.25)*math.cos(3*t)-math.cos(4*t))*(-1)-(r//5)
        return (ax, ay)

class Astar(Aellipse):
    """an animated star
    :param x: x coordinate of the center of the star.
    :param y: y coordinate of the center of the star.
    :param points: number of points of the star.
    :param radius: radius in pixel.
    :param angle_offset : angle in degrees to rotate the shape counter-clockwise. 
                          default = 0 = first point pointing East.
    :param outline: The outline of the heart. Must be a hex value for a color.
    :param colors: Number of colors used in the bitmap and palette. default 128.
    """
    def __init__(self, x, y, points, radius, *,jump=2, angle_offset=0, outline=None, colors=128, stroke=1):
        self.stroke = stroke
        self.width = self.height = radius*2+1
        self.closed = True
        self._palette = displayio.Palette(colors)
        self._palette.make_transparent(0)
        self._bitmap = displayio.Bitmap(self.width, self.height, colors)
        self._conversion_table = []

        if outline is not None:
            self._palette[1] = outline
            point_list = []
            step = 360 / points
            theta = -90
            while theta < 270 :
                ax, ay = self._curveplot(radius, radius, theta)
                if angle_offset != 0:
                    off_r = math.radians(angle_offset)
                    nx = ax * math.cos(off_r) + ay * math.sin(off_r)
                    ny = -ax * math.sin(off_r) + ay * math.cos(off_r)
                    ax = nx
                    ay = ny
                ax = int(round(ax + self.width/2,0))
                ay = int(round(ay + self.height/2,0))
                point_list.append((ax,ay))
                theta += step
            a = None
            b = None
            for i in range(0,len(point_list)):
                if a is None:
                    a = 0
                else:
                    a = b
                b = a+jump
                if b >= points:
                    b = b - points
                self._line(point_list[a][0], point_list[a][1], point_list[b][0], point_list[b][1], 1)
        else:
            raise RuntimeError("base color must be provided for outline.")
        self.n = len(self._conversion_table) 
        x_offset = x - radius
        y_offset = y - radius
        super(Ashape, self).__init__(
              self._bitmap, pixel_shader=self._palette, x=x_offset, y=y_offset
             )

class Asinwave(Ashape):
    """An animated sin wave.
    :param x: The x-position of the top left corner.
    :param y: The y-position of the top left corner.
    :param width: The width of the area.
    :param height: The height of the area.
    :param phase: Number of phases to draw.
    :param outline: The color of the wave. Must be a hex value for a color.
    :param stroke: Thickness of the lines or points drawn, in pixels.
    :param colors : Number of colors used in the bitmap and palette. default 128.
    :param lines: When set to True, draw lines between points. default = False.
    """
    def __init__(self, x, y, width, height, *, phase=1, outline=None, stroke=1, colors=128, lines=False):
        super().__init__(x, y, width, height, outline=outline, stroke=stroke, colors=colors)
        
        self.phase = phase
        p = 0
        for ax, ay in self._compute_line(0,0,width-1,0):
            ay = self._plotter(ax) 
            by = ay * ((height-self.stroke)/2) * -1 + ((height-self.stroke)/2)
            by = int(round(by))
            if lines:
                if p > 0:
                    self._line(zx,zy,ax,by,1)
                zx, zy = ax, by
                p += 1
            else:
                for i in range(0,self.stroke):
                    if i == 0:
                        pos = self._add_pixel(ax,by)
                    else:
                        self._add_pixel(ax,by+i,position=pos)
        self.fill(outline)
    
    def _plotter(self, x):
        x = x * ((self.phase*2*math.pi)/(self.width-1))
        return math.sin(x)


# TODO : arcs (?) piecharts (?)
#        points
#        sin waves
