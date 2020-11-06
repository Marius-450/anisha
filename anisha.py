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
    :param anim_mode : "vertical", "horizontal" or "circular"
    """

    def __init__(self, x, y, width, height, *, fill=None, outline=None, stroke=1, anim_mode="circular", colors=16):
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
        if self.anim_mode == "circular":
            for w in range(self.width):
                for line in range(self.stroke):
                    self._bitmap[w, line] = 1
                    self._bitmap[w, self.height - 1 - line] = 1
                for _h in range(self.height):
                    for line in range(self.stroke):
                        self._bitmap[line, _h] = 1
                        self._bitmap[self.width - 1 - line, _h] = 1
        else:
            for i in range(self.n):
                for x,y in self._conversion_table[i]:
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
        pixels = {}
        for i in range(0,len(self._palette)):
            pixels[i] = 0
        for x in range(self.width):
            for y in range(self.height):
                pixels[self._bitmap[x,y]] += 1
        for i in range(2,len(self._palette)):
            if pixels[i] == 0:
                self._palette[i] = 0x000000


