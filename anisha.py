#
# Animate Shapes
# by @marius-450
# based on adafruit_display_shapes / adafruit_led_animation  and trying to be
# compatible with matrixportal objects animations
#


import displayio

class Arect(displayio.TileGrid):
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
        self._bitmap = displayio.Bitmap(width, height, colors)
        self._palette = displayio.Palette(colors)

        self.width = width
        self.height = height
        self.stroke = stroke
        self.anim_mode=anim_mode

        if outline is not None:
            self._palette[1] = outline
            for w in range(width):
                for line in range(stroke):
                    self._bitmap[w, line] = 1
                    self._bitmap[w, height - 1 - line] = 1
            for _h in range(height):
                for line in range(stroke):
                    self._bitmap[line, _h] = 1
                    self._bitmap[width - 1 - line, _h] = 1
        else:
            raise RuntimeError("base color must be provided for outline.")

        if fill is not None:
            self._palette[0] = fill
            self._palette.make_opaque(0)
        else:
            self._palette[0] = 0
            self._palette.make_transparent(0)

        self._conversion_table = {}

        if self.anim_mode == "circular":
            self.n = (self.width * 2) + (self.height - self.stroke * 2)*2
            corner0 = 0
            corner1 = self.width
            corner2 = self.width + self.height - self.stroke
            corner3 = self.width *2 + self.height - self.stroke*2
            for n in range(0, self.n):
                self._conversion_table[n] = []
                if n < corner1:
                    for p in range(0, self.stroke):
                        self._conversion_table[n].append((n,p))
                elif n < corner2:
                    for p in range(0, self.stroke):
                        self._conversion_table[n].append((self.width - 1 - p, n - self.width + self.stroke))
                elif n < corner3:
                    for p in range(0, self.stroke):
                        self._conversion_table[n].append((self.width - (1 + self.stroke) - (n - corner2), (self.height - 1) - p))
                else:
                    for p in range(0, self.stroke):
                        self._conversion_table[n].append((p,self.height - (n - corner3 ) - (1 + self.stroke)))

        elif self.anim_mode == "horizontal":
            self.n = self.width
            for n in range(0, self.n):
                self._conversion_table[n] = []
                for p in range(0, self.height):
                    self._conversion_table[n].append((n,p))
        elif self.anim_mode == "vertical":
            self.n = self.height
            for n in range(0, self.n):
                self._conversion_table[n] = []
                for p in range(0, self.width):
                    self._conversion_table[n].append((p,n))
        else:
            print("Error : anime_mode '",self.anim_mode ,"' not recognised. use 'circular', 'horizontal' or 'vertical'")
            raise RuntimeError('anime mode not recognised')
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
        self._palette[1] = color
        for index, points in self._conversion_table.items():
            for p in points:
                x = p[0]
                y = p[1]
                self._bitmap[x,y] = 1

        for i in range(2,len(self._palette)):
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
                for i in range(0,len(self._palette)):
                    print(i , " : ", self._palette[i])
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
        r,g,b,w = self._parse_color( self._bitmap[self._conversion_table[index][0]])
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
        pixels = [0] * len(self._palette)
        for x in range(self.width):
            for y in range(self.height):
                pixels[self._bitmap[x,y]] += 1
        for i in range(2,len(self._palette)):
            if pixels[i] == 0:
                self._palette[i] = 0x000000


class Apoly(Arect):
    """An animated polygon.
    :param points: A list of (x, y) tuples of the points
    :param outline: The outline of the polygon. Must be a hex value for a color
    :param colors: Number of colors used in the bitmap and palette. default 128.
    :param closed : Boolean indicating if the shape is closed or not.
    """
    def __init__(self, points, *, outline=None, colors=128, closed=True):
        xs = []
        ys = []
        self._conversion_table = {}
        self.closed = closed

        for point in points:
            xs.append(point[0])
            ys.append(point[1])

        x_offset = min(xs)
        y_offset = min(ys)

        # Find the largest and smallest X values to figure out width for bitmap
        self.width = max(xs) - min(xs) + 1
        self.height = max(ys) - min(ys) + 1

        self._palette = displayio.Palette(colors)
        self._palette.make_transparent(0)
        self._bitmap = displayio.Bitmap(self.width, self.height, colors)

        if outline is not None:
            # print("outline")
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
        super(Arect, self).__init__(
            self._bitmap, pixel_shader=self._palette, x=x_offset, y=y_offset
        )

    # pylint: disable=invalid-name, too-many-locals, too-many-branches
    def _line(self, x0, y0, x1, y1, color):
        reverse = False
        buffer = []
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
                reverse = True
            for _h in range(y0, y1 + 1):
                self._bitmap[x0, _h] = color
                if reverse:
                    buffer.append((x0,_h))
                else:
                    self._conversion_table[len(self._conversion_table)] = [(x0,_h)]
        elif y0 == y1:
            if x0 > x1:
                x0, x1 = x1, x0
                reverse = True
            for _w in range(x0, x1 + 1):
                self._bitmap[_w, y0] = color
                if reverse:
                    buffer.append((_w,y0))
                else:
                    self._conversion_table[len(self._conversion_table)] = [(_w,y0)]
        else:
            steep = abs(y1 - y0) > abs(x1 - x0)
            if steep:
                x0, y0 = y0, x0
                x1, y1 = y1, x1

            if x0 > x1:
                reverse = True
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            dx = x1 - x0
            dy = abs(y1 - y0)

            err = dx / 2

            if y0 < y1:
                ystep = 1
            else:
                ystep = -1

            for x in range(x0, x1 + 1):
                if steep:
                    self._bitmap[y0, x] = color
                    if reverse:
                        buffer.append((y0, x))
                    else:
                        self._conversion_table[len(self._conversion_table)] = [(y0,x)]
                else:
                    self._bitmap[x, y0] = color
                    if reverse:
                        buffer.append((x,y0))
                    else:
                        self._conversion_table[len(self._conversion_table)] = [(x,y0)]
                err -= dy
                if err < 0:
                    y0 += ystep
                    err += dx
        if reverse:
            while len(buffer) > 0:
                x,y = buffer.pop()
                self._conversion_table[len(self._conversion_table)] = [(x,y)]


class Atriangle(Apoly):
    """An animated triangle.
    :param x0, y0: First point coordinates
    :param x1, y1: Second point coordinates
    :param x2, y2: Third point coordinates
    :param outline: The outline of the triangle. Must be a hex value for a color
    :param colors: Number of colors used in the bitmap and palette. default 128.
    """
    def __init__(self, x0, y0, x1, y1, x2, y2, *, outline=None, colors=128):
        super().__init__([(x0, y0),(x1, y1),(x2, y2)], outline=outline, colors=colors, closed=True)



class Aline(Apoly):
    """An animated line.
    :param x0, y0: First point coordinates
    :param x1, y1: Second point coordinates
    :param outline: The color of the line. Must be a hex value for a color
    :param colors: Number of colors used in the bitmap and palette. default 128.
    """
    def __init__(self, x0, y0, x1, y1, *, outline=None, colors=128):
        super().__init__([(x0, y0),(x1, y1)], outline=outline, colors=colors, closed=False)




# TODO : ellipses cicles arcs piecharts
#        regular polygons
#        points
