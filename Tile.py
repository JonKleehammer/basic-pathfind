import random
import numpy

# a file that holds the class Tile and all of its methods

class Tile:

    # start and goal tiles are held within the class and are initially null
    start_tile = None
    goal_tile = None

    # on initialization takes an x and y coordinate
    def __init__(self, x, y):

        self.x = x
        self.y = y

        # color starts as black, then the generic set_color method is called to create a checkerboard
        self.color = (0, 0, 0)
        self.set_color()

        # To be used to point to the tile with the lowest score
        self.parent = None

        # heuristic estimate of square
        self.h = 0
        # real cost to square
        self.g = 0
        # combined g + h
        self.f = None

        # default not obstacle, but is randomly chosen
        self.obstacle = False
        if 0 == random.randint(0, 3):
            self.obstacle = True
            self.set_color((0, 0, 0))

    # method for setting the color, takes an overload for rgb to specify color
    def set_color(self, rgb=None):
        if rgb is None:
            if (self.x + self.y) % 2 == 0:
                self.color = (255, 255, 255)
            else:
                self.color = (200, 200, 240)
        else:
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

            r = numpy.clip(r, 0, 255)
            g = numpy.clip(g, 0, 255)
            b = numpy.clip(b, 0, 255)

            self.color = (r, g, b)

    # adjust color changes the color relative to the current value (eg (-20, 0, 0) reduces the red value by 20
    def adjust_color(self, rgb):

        r = self.color[0] + rgb[0]
        g = self.color[1] + rgb[1]
        b = self.color[2] + rgb[2]

        r = numpy.clip(r, 0, 255)
        g = numpy.clip(g, 0, 255)
        b = numpy.clip(b, 0, 255)

        self.color = (r, g, b)

    def get_color(self):
        return self.color

    # setting the tile to start (also sets the color and makes it not an obstacle)
    def set_start(self):
        self.obstacle = False
        Tile.start_tile = self
        self.color = (0, 255, 0)

    # setting the tile to goal (also sets the color and makes it not an obstacle)
    def set_goal(self):
        self.obstacle = False
        Tile.goal_tile = self
        self.color = (255, 255, 0)