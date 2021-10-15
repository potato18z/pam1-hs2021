# Author:      Matthias Frey
#              Sichen Li
# Created:     28. August 2016
# Updated:     15. October 2021
#
# Python naming convention:
#   All functions and variables that are given with two
#   leading underscores "__" should be considered as
#   private member functions, respectively, variables.

import numpy as np

from AcceLEGOrator.Distribution import *
from AcceLEGOrator.Particle import *

class Bunch(object):
    """
    A class that specifies a bunch of particles
    Ordering of the state vector: (x, px, z, py, z, pz)

    Attributes
    ----------
    __dict : dict
        the mapping of coordinates to indices
    particles : array of (6, N)
        the 6-vectors of N particles
    ptype : Particle
        a specific type of particle, a class inherited from the Particle class
    ekin : array of (N,)
        kinetic energy of all particles

    Methods
    -------
    create(distribution, N, ptype, ekin)
        create N particles of ptype with energy ekin, following a distribution
    __getitem__(key)
        get one coordinate of all particles
    __str__()
        construct a formatted string of the bunch information
    """

    def __init__(self):
        """Initialize the bunch"""

        self.__dict = {'x': 0, "px": 1,
                       'y': 2, "py": 3,
                       'z': 4, "pz": 5}

        self.particles = None   # (x, px, y, py, z, pz)
        self.ptype     = None   # particle type
        self.ekin      = None   # array, kinetic energy of every particle


    def create(self, distribution, N, ptype, ekin):
        """Create N particles of ptype with energy ekin, following a distribution

        Parameters
        ----------
        distribution : Distribution
            a specific distribution, a class inherited from the Distribution class
        N : int
            The number of particles
        ptype : Particle
            a specific type of particle, a class inherited from the Particle class
        ekin : array of (N,)
            kinetic energy of all particles
        """

        self.particles = distribution.create(N)
        self.ptype = ptype
        self.ekin = ekin * np.ones((N,), dtype=np.float)


    def __getitem__(self, key):
        """Get one coordinate of all particles

        Parameters
        ----------
        key : str
            one of (x, px, y, py, z, pz), specifies the coordinate

        Returns
        -------
            an array of (N,), one specific coordinate of all particles
        """

        return self.particles[self.__dict[key], :]


    def __str__(self):
        """Construct a formatted string of the bunch information

        Returns
        -------
        info
            a string of bunch information
        """

        sign = '*' * 51
        info = sign + '\n'\
               + 'Bunch information:\n' \
               + '         #particles:\t\t' + str(len(self.ekin)) + '\n'\
               + self.ptype + sign
        return info
