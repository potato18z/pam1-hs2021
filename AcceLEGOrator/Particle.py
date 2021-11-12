# Author:      Matthias Frey
#              Sichen Li
# Created:     28. August 2016
# Updated:     15. October 2021

from AcceLEGOrator.Physics import *
from AcceLEGOrator.Constants import *


class Particle(object):
    """The base class of all particles

    Attributes
    ----------
    mass : float
        particle mass in MeV /c^2
    charge : float
        particle charge in e
    pname : str
        a string specifying particle type

    Methods
    -------
    __str__()
        construct a formatted string of particle information
    """

    def __init__(self, mass, charge, pname):
        self.mass = mass        # MeV / c^2
        self.charge = charge    # e
        self.pname = pname      # string specifying type

    def __str__(self):
        info =   '           particle:\t\t' + self.pname + '\n'\
               + '             * charge:\t\t' + str(self.charge * Constants.echarge) + ' C\n'\
               + '             *   mass:\t\t' + str(self.mass) + ' MeV/c^2\n'
        return info

class Proton(Particle):

    def __init__(self):
        super(Proton, self).__init__(Constants.pmass,
                                     1.0,
                                     'Proton')

class Electron(Particle):

    def __init__(self):
        super(Electron, self).__init__(Constants.emass,
                                       -1.0,
                                       'Electron')
