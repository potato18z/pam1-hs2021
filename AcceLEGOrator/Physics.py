# Author:   Sichen Li
# Created:     17. September 2019
# Updated
#
# This file defines the physic relations
# used in particle accelerator computations.

import numpy as np

class Physics:
    # return the relativistic factor
    # @param ekin is the kinetic energy in MeV
    # @param mass is the particle mass in MeV/c^2
    def getGamma(ekin, mass):
        return ekin / mass + 1.0

    # return beta ( velocity / clight)
    # @param gamma is the relativistic factor
    def getBeta(gamma):
        return np.sqrt( 1.0 - 1.0 / gamma ** 2 )
