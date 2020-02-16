"""
TextRPGLib - Made by Davidluke1701, please give me credit if you want to use this in your project, I would be happy to see it (=
"""


from scrtools import stream
from scrtools import color
from blessed import Terminal; t = Terminal()
import pickle
import sys

class data:
    """backend collections"""
    def save(self, file):
        with open(file, "wb") as f:
            pickle.dump(self, f)
    @staticmethod
    def load(file):
        with open(file, "rb") as f:
            return pickle.load(f)

class frontend:
    """Frontend collections"""
    title_color = color("steelblue2")
    subtitle_color = color("dodgerblue4")


    @staticmethod
    def flavortext(body, delay_ms, *, end=None, factor = 10):
        if end == None:
            end = ''
        stream.echo("  *" + " "* int(stream.width()/factor), 0, end='')
        _ = stream.echo(body, delay_ms, end=end)
        return _
        del end
    @classmethod
    def setting(cls, title, subtitle, t_delay_ms, s_delay_ms):
        e = cls.flavortext(cls.title_color.w(title), t_delay_ms, end='\n')
        if e != 0:
            cls.flavortext(cls.subtitle_color.w(subtitle), s_delay_ms)
        elif e == 0:
            cls.flavortext(cls.subtitle_color.w(subtitle), 0)
    @classmethod
    def block(cls, body, delay_ms, downtime, *, end=None, check=None, cont=False, factor=10, begin=None):
        if check == None:
            sys.stdout.write(t.move_y(8))
        if begin != None:
            sys.stdout.write(begin)
        mone = False
        if check:
                delay_ms = 0
                downtime = 0
                mone = True
        if end==None:
                end = '\n'
        for thing in body:
                if thing == "\n" or thing == ("\n") or thing == ["\n"]:
                    e = stream.echo(thing, delay_ms, end=end)
                elif cont:
                    e = stream.echo(thing, delay_ms, end=end)
                elif not cont:
                    e = cls.flavortext(thing, delay_ms, end=end, factor=factor)
                if e:
                    delay_ms = 0
                    downtime = 0
                    mone = True
                if not (thing == "\n" or thing == ("\n") or thing == ["\n"]):
                    stream.wait(timeout_ms = downtime)
        return mone