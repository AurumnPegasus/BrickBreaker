from constants import *

class Brick (object):
    def __init__(self, tiles):
        self.tiles = tiles

    def type(self, arg):
        for key, value in self.tiles.items():
            if value == arg:
                return key
        
        return None

class One (Brick):
    def __init__(self, tiles):
        Brick.__init__(self, tiles)

    def reduce(self, arg):
        return ' '

class Two (Brick):
    def __init__(self, tiles):
        Brick.__init__(self, tiles)

    def reduce(self, arg):
        if arg == '[' or arg == ']':
            return arg
        return '+'

class Three (Brick):
    def __init__(self, tiles):
        Brick.__init__(self, tiles)

    def reduce(self, arg):
        if arg == '[' or arg == ']':
            return arg
        return '-'

class Four (Brick):
    def __init__(self, tiles):
        Brick.__init__(self, tiles)

    def reduce(self, arg):
        if arg == '[' or arg == ']':
            return arg
        return '/'

class Five (Brick):
    def __init__(self, tiles):
        Brick.__init__(self, tiles)

    def reduce(self, arg):
        if arg == '[' or arg == ']':
            return arg
        return '#'

