import numpy as np
import itertools
from random import random as RNG

#Here we will implement some MC integration algorithm

#We will first deal with basic shapes that we integrate over

class polygon():

    '''This is a simple polygon class. Contains methods to determine wether a point is inside the shape or not.'''

    def __init__(self, points):

        '''polygon(points): points is a list of 2D tuples that marks the points that outline the polygon. The points are to form a line with the last point connecting back to the first.'''

        self.points = np.array(points)
        self.lines = []

        for i,p in enumerate(self.points):

            self.lines.append(self.line_maker(self.points[i-1], p))

        self.minx   = min([x[0] for x in self.points])
        self.maxx   = max([x[0] for x in self.points])
        self.miny   = min([x[1] for x in self.points])
        self.maxy   = max([x[1] for x in self.points])

    def is_inside(self,point):

        '''is_inside(point): point is a 2D tuple that marks a point. The method returns a boolean that tells you if the point is inside the polygon.'''

        intersections = 0

        #we now define a line coming to the point we test from the negative y axis

        for i,l in enumerate(self.lines):

            if l(point[0]) > point[1]: #line intersects with outline south of point

                if (self.points[i-1][0] < point[0] and self.points[i][0] > point[0]) or (self.points[i-1][0] > point[0] and self.points[i][0] < point[0]): #intersection is on segment

                    intersections += 1

        return bool(intersections//2)

    def line_maker(p1, p2):

        '''line_maker(p1, p2): Returns a function that defines a line going through the 2D points p1 and p2'''

        a = (p1[1] - p2[1])/(p1[0] - p2[0])

        b = p1[1] - a * p1[0]

        def f(x):

            return (a * x + b)

        return f

#For homework: Add class for circle, function, mouse and cat


class Integrator():

    def __init__(self, shapes):

        '''Integrator(shapes) takes in shape class instances like polygon or circle and integrates the combined area, intersection or exclusion.'''

        if isinstance(shapes,list):

            self.shapes = shapes

        else:

            self.shapes = [shapes]

        self.minx   = min([x.minx for x in self.shapes])
        self.maxx   = max([x.maxx for x in self.shapes])
        self.miny   = min([x.miny for x in self.shapes])
        self.maxy   = max([x.maxy for x in self.shapes])

        self.basearea = (self.maxx - self.minx)*(self.maxy - self.miny)

    def Combined(self, npoints = 10000):

        '''Combined(npoints = 10000): This function returns the combined area of all shapes attached to the current instance. npoints is the number of MC points used for the integral'''

        total = 0

        for _ in itertools.repeat(None, npoints):

            for sh in self.shapes:

                if sh.is_inside(self.GenPoint):

                    total += 1

                    break

        return(self.basearea * total / npoints)

#For homework: add intersection and weighted integral

    def GenPoint(self):

        '''GenPoint(): This function generates an MC point within the relevant area.'''

        return (self.minx + RNG()*(self.maxx - self.minx),self.miny + RNG()*(self.maxy - self.miny))
