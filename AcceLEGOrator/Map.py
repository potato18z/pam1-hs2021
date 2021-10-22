# Author:   Matthias Frey/Sichen Li
# Date:     28. August 2016
#
# This file defines Base class of all maps.
# Additional maps need to inherit from it.

from abc import abstractmethod
import numpy as np

class Map(object):
    """The base class of Map (doc under construction)
    """

    def __init__(self, R, length):
        self.R = np.matrix(R)
        self.length = length

    def __str__(self):
        return '\n'

    def __mul__(self, other):
        return self.R * other

    def __rmul__(self, other):
        return other * self.R

    def __sub__(self, other):
        return other - self.R

    def __rsub__(self, other):
        return self.R - other

    def __add__(self, other):
        return other + self.R

    def __radd__(self, other):
        return self.R + other

    def __pow__(self, other):
        return self.R ** other

    @abstractmethod
    def get(self, length):
        pass
