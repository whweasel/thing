
"""
Screentools - 4.9 Beta. 
If you want to use this in your project, contact me via reddit. I would be more than happy to see what you've come up with (=
"""


import gc
from blessed import Terminal;t = Terminal()
import sys
import random
import string

class painted:
    def __init__(self, color, text):
        self.color = color
        self.text = text
    def __str__(self):
        return self.text

class color:
    def __init__(self, color):
        self.color = getattr(t,color)
    def w(self, text):
        return painted(self.color, text)
class MemoryError(Exception):
    pass
class stream:
    """I/O Stream"""
    fullscreen = t.fullscreen
    # ==> Properties of the Terminal <== #
    @staticmethod
    def width():
        return t.width
    @staticmethod
    def height():
        return t.height
    number_of_colors = t.number_of_colors
    # ==> Keyboard < == #
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
    keycodes = {
        " ":"KEY_SPACE",
        ".":"KEY_PERIOD",
        ",":"KEY_COMMA",
        "/":"KEY_SLASH",
        ";":"KEY_SEMICOLON",
        "'":"KEY_QUOTE",
        "`":"KEY_TICK",
        "-":"KEY_HYPHEN",
        "=":"KEY_EQUALS",
        "[":"KEY_OPENBRACE",
        "]":"KEY_CLOSEBRACE",
        "\\":"KEY_BACKSLASH",
        "+":"KEY_ADD",
        "*":"KEY_ASTERISK"
    }
    echo_escape_keys = []
    # ==> Menu <== #
    menu_cursor_color = t.bright_white
    menu_highlight_color = t.bright_white
    menu_cursor = "*"
    menu_select_keys = ["KEY_ENTER"]
    sleep_escape_keys = ["KEY_ENTER"]

    @classmethod
    def wait(cls, *, timeout_ms =None):
        if timeout_ms != None:
            timeout_ms = timeout_ms / 1000
        with t.raw():#wait for keyboard input
            k = t.inkey(timeout=timeout_ms)
        if k._name != None:
            if "KEY_" in k._name:
                return k._name
        elif k in cls.alphabet:
            return "KEY_" +k.upper()
        elif k in cls.keycodes:
            return cls.keycodes[k]
    # ==> Out <== #
    default_end = ''
    @staticmethod
    def clear():
        sys.stdout.write(t.clear + t.home)
    @staticmethod
    def collect():
        gc.collect()
        try:
            del gc.garbage[:]
        except:
            pass

    @classmethod
    def write(cls, body, *, end=None):
        if end == None:
            end = cls.default_end
        if type(body) == int:
            sys.stdout.write(str(body))
            sys.stdout.flush()
            sys.stdout.write(end)
        elif type(body) == str:
            sys.stdout.write(body)
            sys.stdout.flush()
            sys.stdout.write(end)
        elif type(body) == painted:
                sys.stdout.write(body.color)
                for char in body.text:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                sys.stdout.write(t.normal)
        elif type(body) == tuple or type(body) == list:
            for item in body:
                if type(item) == tuple or type(item) == list:
                    sys.stdout.write(str(item))
                    sys.stdout.flush()
                elif type(item) == int:
                    for char in str(item):
                        sys.stdout.write(char)
                        sys.stdout.flush()
                elif type(item) == str:
                    for char in item:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                elif type(item) == painted:
                    sys.stdout.write(item.color)
                    for char in item.text:
                        sys.stdout.write(char)
                        sys.stdout.flush()
            sys.stdout.write(t.normal + end)
            sys.stdout.flush()
    @classmethod
    def echo(cls, body, delay_ms=34, *, end=None):
        skip = False
        pressedKey = "KEY_"
        if end == None:
            end = cls.default_end
        if type(body) == tuple or type(body) == list:
            for item in body:
                if type(item) == tuple or type(item) == list:
                    msg = t.bright_red("cannot echo a list or tuple, which contains either lists or tuples")
                    raise MemoryError(msg)
                elif type(item) == int:
                    for char in str(item):
                        if str(item)[0] == char:
                            sys.stdout.write(char)
                            continue
                        if delay_ms != 0:
                            pressedKey = cls.wait(timeout_ms = delay_ms)
                            if pressedKey in cls.echo_escape_keys:
                                delay_ms = 0
                                skip = True
                        sys.stdout.write(char)
                        sys.stdout.flush()
                elif type(item) == str:
                    for char in item:
                        if delay_ms != 0:
                            pressedKey = cls.wait(timeout_ms = delay_ms)
                            if pressedKey in cls.echo_escape_keys:
                                delay_ms = 0  
                                skip = True
                        sys.stdout.write(char)
                        sys.stdout.flush()
                elif type(item) == painted:
                    sys.stdout.write(item.color)
                    for char in item.text:
                        if delay_ms != 0:
                            pressedKey = cls.wait(timeout_ms = delay_ms)
                            if pressedKey in cls.echo_escape_keys:
                                delay_ms = 0
                        sys.stdout.write(char)
                        sys.stdout.flush()
                    sys.stdout.write(t.normal)  
        if type(body) == int:
            for char in str(body):
                if delay_ms != 0:
                    pressedKey = cls.wait(timeout_ms = delay_ms)
                    if pressedKey in cls.echo_escape_keys:
                        delay_ms = 0
                        skip = True
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write(end)
            sys.stdout.flush()
        elif type(body) == str:
            for char in body:
                if delay_ms != 0:
                    pressedKey = cls.wait(timeout_ms = delay_ms)
                    if pressedKey in cls.echo_escape_keys:
                        delay_ms = 0
                        skip = True
                sys.stdout.write(char)
                sys.stdout.flush()
        elif type(body) == painted:
            sys.stdout.write(body.color)
            for char in body.text:
                if delay_ms != 0:
                    pressedKey = cls.wait(timeout_ms = delay_ms)
                    if pressedKey in cls.echo_escape_keys:
                        delay_ms = 0
                        skip = True
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write(t.normal)
        sys.stdout.write(end)
        sys.stdout.flush()
        return skip
    @classmethod
    def bruteforce(cls, target, delay_ms, *, color=t.normal, end=None, begin=""):
        sys.stdout.write(t.move_y(8))
        stream.echo("  *" + " "* int(stream.width()/10) + begin)
        val = t.get_location()
        
        
        if end == None:
            end = cls.default_end
        delay_ms = delay_ms / 1000
        if type(color) == color:
            color = color.color
        elif type(color) == str:
            color = getattr(t, color)
        guess = list(' '*len(target))
        for i, c in enumerate(target):
            while True:
                cc = random.choice(string.ascii_letters + string.punctuation + " ")
                guess[i] = cc
                sys.stdout.write(color)
                sys.stdout.write(t.move_xy(val[1], val[0]) + f"{''.join(guess)}")
                sys.stdout.flush()
                cls.wait(timeout_ms = delay_ms)
                if cc == c:
                    sys.stdout.write(t.normal)
                    break
    @classmethod
    def menu(cls, header, content, *, kind="vertical", delay_ms = 34, factor=4, tfactor = 5):
        if type(cls.menu_cursor_color) == color:
            cls.menu_cursor_color = cls.menu_cursor_color.color
        if type(cls.menu_highlight_color) == color:
            cls.menu_highlight_color = cls.menu_highlight_color.color
        
        cls.menu_cursor_position = 1
        cls.clear()
        whileLoopIter = -1
        while kind == "vertical":
            whileLoopIter += 1
            menu_iteration = 0
            if whileLoopIter > 0:
                sys.stdout.write(t.home)
                sys.stdout.write(("   " + " "* int(stream.width()/tfactor)) + "  " + header)
                sys.stdout.write("\n")
            elif whileLoopIter == 0:
                stream.echo("   " + " "* int(stream.width()/tfactor), 0, end='')
                cls.echo("  " + header, delay_ms, end='\n')
            for item in content:
                menu_iteration += 1
                if cls.menu_cursor_position == menu_iteration:
                    print(("   " + " "* int(stream.width()/factor)) + "{} {}".format(cls.menu_cursor_color(cls.menu_cursor), ""+ cls.menu_highlight_color(item)), end='\n')
                elif cls.menu_cursor_position != menu_iteration:
                    if type(item) == painted:
                        item = item.color(item.text)
                    print(("   " + " "* int(stream.width()/factor)) + "  {}".format(item), end='\n')
            key = cls.wait()
            if key == "KEY_UP":
                if cls.menu_cursor_position <= 1:
                    cls.menu_cursor_position = len(content)
                elif cls.menu_cursor_position > 1:
                    cls.menu_cursor_position -= 1
                continue
            if key == "KEY_DOWN":
                if cls.menu_cursor_position >= len(content):
                    cls.menu_cursor_position = 1
                elif cls.menu_cursor_position >= 1:
                    cls.menu_cursor_position +=1
                continue
            elif key in cls.menu_select_keys:
                return cls.menu_cursor_position
    @classmethod
    def sleep(cls, time_ms, *, allow_escape = False):
        cls.collect()
        time_ms = (time_ms * .80) - 1
        with t.raw():
            i = 0
            while True:
                    i = i+1
                    pressedKey = stream.wait(timeout_ms = 1)
                    print(i)
                    if pressedKey in cls.sleep_escape_keys and allow_escape:
                        return True
                    if pressedKey == "KEY_":
                        pass
                    if i == time_ms:
                        break
        return False


    @classmethod
    def pause(cls):
        delay_ms = 1
        with t.raw():
            while True:
                    pressedKey = t.inkey(timeout =delay_ms / 1000)
                    if pressedKey.is_sequence:
                        pressedKey = pressedKey.name
                    elif pressedKey in cls.keycodes:
                        pressedKey = cls.keycodes[pressedKey]
                    else:
                        pressedKey = "KEY_"+str(pressedKey).upper()
                    if pressedKey in cls.sleep_escape_keys:
                        return True
        return False


class colors:
    ### Default Colors ###
    red = color("red1")
    yellow = color("gold2")
    orange = color("darkorange2")
    purple = color("darkorchid1")
    blue = color("blue3")
    cyan = color("turquoise3")
    green = color("chartreuse3")

    gray = color("gray30")
    ### Extra Colors ###
    lightblue = color("royalblue2")
    slateblue = color("slateblue1")
    magenta = color("maroon2")
    lightred = color("firebrick1")
class symbols:
    ### Standard Symbols ###
    copyright = u"\u00A9"
    registered = u"\u00AE"
    trademark = u"\u2122"
    semi_cc = u"\u21B6"
    semi_c = u"\u21B7"
    x_box = u"\u2327"
    keyboard = u"\u2328"
    eject = u"\u23CF"
    triangle = u"\u25B6"
    starandcrescent = u"\u262A"
    radioactive = u"\u2622"
    biohazard = u"\u2623"
    hammerandsickle = u"\u262D"
    plane = u"\u2708"
    sixpointstar = u"\u2721"
    frenchflag = u"\U0001F3F3"


