import numpy as np
import math

class Bone:
    def __init__(self, length, translation = (0,0), rotation = 0, color = (0,0,0)):
        self.length = length
        self.translation = translation
        self.rotation = rotation
        self.parent = None
        self.children = []
        self.color = color

    def transform_matrix(self):
        c = math.cos(self.rotation)
        s = math.sin(self.rotation)

        mat = np.matrix([
            [c,-s, self.translation[0]],
            [s, c, self.translation[1]],
            [0,0,1]
        ])

        if self.parent is None:
            return mat

        return self.parent.transform_matrix() * mat

    def add_child(self, c):
        c.parent = self
        self.children.append(c)

    def start(self):
        p = np.matrix(((0,), (0,), (1,)))

        return self.transform_matrix() * p

    def end(self):
        if self.parent is None:
            p = np.matrix(((0,), (0,), (1,)))
        else:
            p = np.matrix(((0,), (self.parent.length,), (1,)))

        translation = np.matrix([[0, 0, 0],
                                 [0, 0, self.length],
                                 [0, 0, 1]])

        return self.transform_matrix() * translation * p

    def position_start(self):
        p = self.start()
        return (p[0], p[1])

    def position_end(self):
        p = self.end()
        return (p[0], p[1])

    def rotate(self, angles):
        """
        Angles donnés en preorder
        """
        rotation = angles[0]
        others = angles[1:]

        self.rotation = rotation

        for c in self.children:
            others = c.rotate(others)

        # if len(others) != 0 and self.parent is None:
        #     raise Exception("Too many angles")

        return others

    def __str__(self):
        return str((self.position_start(), self.position_end()))
