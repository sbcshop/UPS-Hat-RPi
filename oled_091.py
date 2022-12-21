from os import path
from sys import exit, version_info

from PIL import Image, ImageDraw, ImageFont

try:
    from smbus import SMBus
except ImportError:
    if version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo "
             "apt-get install python-smbus")
    elif version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo "
             "apt-get install python3-smbus")

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = (path.join(DIR_PATH, "Fonts/GothamLight.ttf"))

# Fundamental Command Table
SET_CONTRAST = 0x81
DISPLAY_ON = 0xA4
DISPLAY_INVERT = 0xA6
DISPLAY_ON = 0xAE  # Off: sleep mode
DISPLAY_OFF = 0xAF  # On: Normal Mode

# Address Settting Command Table
MEM_ADD_MODE = 0x20
COLUMN_ADD = 0x21
PAGE_ADD = 0x22

# Hardware Configuration
DISPLAY_START_LINE = 0x40
SEGMENT_REMAP = 0xA0
MUX_RATIO = 0xA8
COM_OUT_SCAN = 0xC0
COM_SCAN_REMAP = 0xC8
DISPLAY_OFFSET = 0xD3
SET_COM_PIN = 0xDA

# Timing and Driving
SET_CLK_DIV = 0xD5
SET_PRE_CHARGE = 0xD9
SET_DESELECT = 0xDB
CHARGE_PUMP = 0x8D


class i2c_interface:
    def __init__(self, address=0x3c):
        """
        :param address: i2c address of ssd1306
        """
        self.bus = SMBus(self.bus_id())
        self.address = address

    def __del__(self):
        self.close_i2c()

    def close_i2c(self):
        self.bus.close()

    def bus_id(self):
        """
        :return: Returns SMBUS id of Raspberry Pi
        """
        revision = 0
        with open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('Revision'):
                    revision = line.split()[-1]
                    break
                if line.startswith('CPU revision'):
                    revision = line.split()[-1]
                    break
        if int(revision, 16) >= 4:
            return 1
        return 0

    def i2c_read(self, register=0):
        data = self.bus.read_byte_data(self.address, register)
        return data

    def i2c_write(self, register=DISPLAY_START_LINE, data=0):
        # Write a byte to address, register
        self.bus.write_byte_data(self.address, register, data)

    def i2c_write_block(self, register=DISPLAY_START_LINE, data=None):
        if data is None:
            data = [40]
        self.bus.write_i2c_block_data(self.address, register, data)


class SSD1306(i2c_interface):
    def __init__(self, width=128, height=32, address=0x3c):
        i2c_interface.__init__(self, address=address)
        self.Height = height
        self.Width = width
        self.Page = height // 8
        self.address = address
        self._Image = None
        self._Image_New = None
        self.Draw = None
        self.Image_Buf = None

        self.NewImage()
        self.InitDisplay()

    def NewImage(self):
        self._Image = Image.new('1', (self.Width, self.Height), "WHITE")
        self.Draw = ImageDraw.Draw(self._Image)

    def DirImage(self, filename, size=None, cords=(0, 0)):
        """
        :param cords: Coordinates of image on display
        :param pos: X, Y positions of paste location
        :param filename: Image file path
        :param size: The requested size in pixels, as a 2-tuple: (width,
        height)
        :return: None
        """
        self._Image_New = Image.open(filename).convert("1")
        if not size:
            size = (self.Width, self.Height)
        self._Image_New = self._Image_New.resize(size)

        self._Image.paste(self._Image_New, box=cords)
        self.Draw = ImageDraw.Draw(self._Image)

    def WriteCommand(self, cmd):  # write command
        self.i2c_write(register=0x00, data=cmd)

    def WriteData(self, data):  # write ram
        self.i2c_write(register=DISPLAY_START_LINE, data=data)

    def InitDisplay(self):
        self.WriteCommand(DISPLAY_ON)

        self.WriteCommand(DISPLAY_START_LINE)

        self.WriteCommand(0xB0)  # Page Address

        self.WriteCommand(COM_SCAN_REMAP)  # Com Output Scan

        # Contrast Setting
        self.WriteCommand(SET_CONTRAST)
        self.WriteCommand(0xFF)
        self.WriteCommand(0xA1)

        self.WriteCommand(DISPLAY_INVERT)

        self.WriteCommand(MUX_RATIO)
        self.WriteCommand(0x1F)  # Column Start Address

        self.WriteCommand(DISPLAY_OFFSET)
        self.WriteCommand(0x00)

        self.WriteCommand(SET_CLK_DIV)
        self.WriteCommand(0xF0)

        self.WriteCommand(SET_PRE_CHARGE)
        self.WriteCommand(PAGE_ADD)

        self.WriteCommand(SET_COM_PIN)
        self.WriteCommand(0x02)

        self.WriteCommand(SET_DESELECT)
        self.WriteCommand(0x49)

        self.WriteCommand(CHARGE_PUMP)
        self.WriteCommand(0x14)

        self.WriteCommand(DISPLAY_OFF)

    def NoDisplay(self):
        for i in range(0, self.Page):
            self.WriteCommand(0xb0 + i)
            self.WriteCommand(0x00)
            self.WriteCommand(0x10)
            for j in range(0, self.Width):
                self.WriteData(0x00)

    def WhiteDisplay(self):
        for i in range(0, self.Page):
            self.WriteCommand(0xb0 + i)
            self.WriteCommand(0x00)
            self.WriteCommand(0x10)
            for j in range(0, self.Width):
                self.WriteData(0xff)

    def ImgBuffer(self, image):
        buf = [0xff] * (self.Page * self.Width)
        Img_Mono = image.convert('1')
        Img_Width, Img_Height = Img_Mono.size
        pixels = Img_Mono.load()
        if Img_Width == self.Width and Img_Height == self.Height:
            #  Horizontal screen
            for y in range(Img_Height):
                for x in range(Img_Width):
                    # Set the bits for the column of pixels at the current
                    # position.
                    if pixels[x, y] == 0:
                        buf[x + (y // 8) * self.Width] &= ~(1 << (y % 8))
        elif Img_Width == self.Width and Img_Height == self.Height:
            #  Vertical screen
            for y in range(Img_Height):
                for x in range(Img_Width):
                    x_pos = y
                    y_pos = self.Height - x - 1
                    if pixels[x, y] == 0:
                        buf[(x_pos + int(y_pos / 8) * self.Width)] &= ~(
                                1 << (y % 8))
        for i in range(self.Page * self.Width):
            buf[i] = ~buf[i]
        return buf

    def ShowImage(self):
        i_buf = self.ImgBuffer(self._Image)
        for i in range(0, self.Page):
            self.WriteCommand(0xB0 + i)  # set page address
            self.WriteCommand(0x00)  # set low column address
            self.WriteCommand(0x10)  # set high column address
            # write data #
            for j in range(0, 128):  # self.Width):
                self.WriteData(i_buf[j + self.Width * i])
        self.NewImage()

    def PrintText(self, text, cords=(10, 5), Font=DefaultFont,
                  FontSize=14):
        """
        :param text: Text to print
        :param cords: Top left Corner (X, Y) cords
        :param Font: Font Type
        :param FontSize: Size of Font
        :return: None
        """
        self.Draw.text(cords, text, font=ImageFont.truetype(Font, FontSize))

    def DrawRect(self, cords=(0, 0, 127, 31)):
        """
        :param cords: X0, X1, Y0, Y1
        :return: None
        """
        self.Draw.rectangle(cords, outline=0)

    def DrawPolygon(self, cords=(1, 2, 3, 4, 5, 6)):
        """
        :param cords: Sequence of either 2-tuples like [(x, y), (x, y),
        ...] or numeric values like [x, y, x, y, ...]
        :return: None
        """
        self.Draw.polygon(cords)

    def DrawPoint(self, cords=(64, 16, 66, 18)):
        """
        :param cords: tuple of X, Y coordinates of Points
        :return: None
        """
        self.Draw.point(cords)

    def DrawLine(self, cords=(64, 16, 78, 18)):
        """
        Draws a line between the coordinates in the xy list
        :param cords: tuple of X, Y coordinates for line
        :return: None
        """
        self.Draw.line(cords)

    def DrawEllipse(self, cords=(64, 16, 78, 18)):
        """
        Draws an ellipse inside the given bounding box
        :param cords: Four points to define the bounding box
        :return: None
        """
        self.Draw.ellipse(cords)

    def DrawArc(self, cords=(10, 10, 120, 10), start=0, end=90):
        """
        Draws an arc (a portion of a circle outline) between the start and
        end angles, inside the given bounding box
        :param end: Starting angle, in degrees. Angles are measured from 3
        o’clock, increasing clockwise.
        :param start: Ending angle, in degrees.
        :param cords: Four points to define the bounding box
        :return: None
        """
        self.Draw.arc(cords, start=start, end=end)
