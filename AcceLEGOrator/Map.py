# Author:   Matthias Frey/Sichen Li
# Date:     5. Nov 2021
#
# This file defines Base class of all maps and some example maps.
# Additional maps need to inherit from it.

from abc import abstractmethod
from AcceLEGOrator import Physics, Constants
import AcceLEGOrator.Parameter as p
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
        """Transfer matrix acting on state vectors.
        """
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

    def __getitem__(self, index):
        return self.R[index]

    def getT(self):
        """
        Returns the transpose of the matrix.

        Does *not* conjugate!
        """
        return self.R.T

    # makes m.T possible
    T = property(getT, None)

# ------------------------------------------------------------------------
# Rotation Map
# ------------------------------------------------------------------------
class Rot(Map):

    def __init__(self, phi):
        self.phi = phi
        cs = np.cos(phi)
        s  = np.sin(phi)

        R = np.matrix([[cs,   0,  s,  0,  0,  0],
                       [0,    cs, 0,  s,  0,  0],
                       [-s,   0,  cs, 0,  0,  0],
                       [0,    -s, 0,  cs, 0,  0],
                       [0,    0,  0,  0,  1,  0],
                       [0,    0,  0,  0,  0,  1]])

        super(Rot, self).__init__(R, 0.0)


    def __str__(self):
        return 'Rot(phi = ' + str(self.phi) + ')\n'


# ------------------------------------------------------------------------
# Fringe Map
# ------------------------------------------------------------------------
class Fringe(Map):

    def __init__(self, k1):
        self.k1 = k1

        R = np.matrix([[1,      0,  0,  0,  0,  0],
                       [-k1,    1,  0,  0,  0,  0],
                       [0,      0,  1,  0,  0,  0],
                       [0,      0,  k1, 1,  0,  0],
                       [0,      0,  0,  0,  1,  0],
                       [0,      0,  0,  0,  0,  1]])
        super(Fringe, self).__init__(R, 0.0)

    def __str__(self):
        return 'Fringe(k1 = ' + str(self.k1) + ')\n'

# ------------------------------------------------------------------------
# Drift Map
# ------------------------------------------------------------------------
class Drift(Map):

    def __init__(self, length):

        beta_0 = Physics.getBeta(p.gamma_0)

        f = length / (beta_0 * p.gamma_0) ** 2

        R = np.matrix([[1, length, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 1, length, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 1, f],
                      [0, 0, 0, 0, 0, 1]])

        super(Drift, self).__init__(R, length)


    def __str__(self):
        return 'Drift(L = ' + str(self.length) + ' [m])\n'


    def get(self, length):
        return Drift(length)


# ------------------------------------------------------------------------
# Dipole
# ------------------------------------------------------------------------
class Dipole(Map):

    # -----------------------------------------------------
    # @param length specified in [m]
    # @param b0 is the vertical magnetic field strength [T]
    # @param phi is the rotation angle in [rad]
    # @param scale is the relation between bending angle
    # and edge angle [number from 0 to 1]
    # -----------------------------------------------------
    def __init__(self, length, b0, phi, scale):

        beta_0  = Physics.getBeta(p.gamma_0)

        self.__b0 = b0
        self.__phi = phi
        self.scale = scale

        c = Constants.clight

        # P_0 = \gamma * \beta * c * m_0 [eV / c]
        P_0 = p.mass * 1e6 / c * p.gamma_0 * beta_0
        w = p.charge / P_0 * self.__b0

        #k1 = -w * np.tan( self.scale * length * w )

        cs   = np.cos(w * length)
        s    = np.sin(w * length)
        f    = length / (beta_0 * p.gamma_0) ** 2
        ibet = 1.0 / beta_0


        D = np.matrix([[cs,         s / w,              0,  0,  0,  (1 - cs) / w * ibet],
                       [-w * s,     cs,                 0,  0,  0,  s * ibet],
                       [0,          0,                  1,  length,  0,  0],
                       [0,          0,                  0,  1,  0,  0],
                       [-s * ibet,  -(1-cs) / w * ibet, 0,  0,  1,  f - (w * length - s) / w * ibet ** 2],
                       [0,          0,                  0,  0,  0,  1]])

        #R = Rot(phi) * Fringe(k1) * D * Fringe(k1) * Rot(-phi)

        R = D

        super(Dipole, self).__init__(R, length)


    def __str__(self):
        return 'Dipole(L = ' + str(self.length) \
               + ' [m], B = ' + str(self.__b0) + ' [T])\n'


    def get(self, length):
        return Dipole(length, self.__b0,
                      self.__phi, self.scale)

# ------------------------------------------------------------------------
# Dipole as Rotation
# ------------------------------------------------------------------------
class DipoleRot(Map):

    def __init__(self, phi):
        self.phi = phi
        cs = np.cos(phi)
        s  = np.sin(phi)
        #beta_0  = Physics.getBeta(p.gamma_0)
    #    ibet = 1.0 / beta_0

        R = np.matrix([[cs,   s,  0,  0,  0,  (1 - cs)],
                       [-s,   cs, 0,  s,  0,  s],
                       [-s,   0,  1, 0,  0,  0],
                       [0,    -s, 0,  1, 0,  0],
                       [-s,  -(1-cs),  0,  0,  1,  0],
                       [0,    0,  0,  0,  0,  1]])

        super(DipoleRot, self).__init__(R, 0.0)


    def __str__(self):
        return 'DipoleRot(phi = ' + str(self.phi) + ')\n'
# ------------------------------------------------------------------------
# Quadrupole
# ------------------------------------------------------------------------
class Quadrupole(Map):

    # -----------------------------------------------------
    # @param length specified in [m]
    # @param gradB is the magnetic field gradient in [T/m]
    # @param phi is the rotation angle [rad]
    # -----------------------------------------------------
    def __init__(self, length, gradB, phi=0.):
        self.__gradB = gradB
        self.__phi = phi

        beta_0  = Physics.getBeta(p.gamma_0)

        c = Constants.clight

        # P_0 = \gamma * \beta * c * m_0 [eV / c]
        P_0 = p.mass * 1e6 / c * p.gamma_0 * beta_0

        w2 = p.charge / P_0 * self.__gradB

        w = np.sqrt( abs(w2) )

        cs  = np.cos(w * length)
        s   = np.sin(w * length)
        csh = np.cosh(w * length)
        sh  = np.sinh(w * length)
        f   = length / (beta_0 * p.gamma_0 ) ** 2

        if w2 > 0:
            # horizontal focusing
            Q = np.matrix([[cs,       s / w,  0,      0,      0,  0],
                           [-w * s,   cs,     0,      0,      0,  0],
                           [0,        0,      csh,    sh / w, 0,  0],
                           [0,        0,      w * sh, csh,    0,  0],
                           [0,        0,      0,      0,      1,  f],
                           [0,        0,      0,      0,      0,  1]])
        else:
            # vertical focusing
            Q = np.matrix([[csh,      sh / w, 0,      0,      0,  0],
                           [w * sh,   csh,    0,      0,      0,  0],
                           [0,        0,      cs,     s / w,  0,  0],
                           [0,        0,      -w * s, cs,     0,  0],
                           [0,        0,      0,      0,      1,  f],
                           [0,        0,      0,      0,      0,  1]])


        R = Rot(phi) * Q * Rot(-phi)

        super(Quadrupole, self).__init__(R, length)


    def __str__(self):
        return 'Quadrupole(L = ' + str(self.length) \
               + ' [m], grad B = ' + str(self.__gradB) + ' [T/m])\n'


    def get(self, length):
        return Quadrupole(length, self.__gradB,
                          self.__phi)


class ThinQuadrupole(Map):

    def __init__(self, f):

        self.f = f

        f = 1.0 / f

        R = np.matrix([[1, 0, 0, 0, 0, 0],
                      [-f, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, f, 1, 0, 0],
                      [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1]])

        super(ThinQuadrupole, self).__init__(R, 0)

    def __str__(self):
        return 'ThinQuadrupole(f = ' + str(self.f) + ' )\n'

    def get(self, length):
        return ThinQuadrupole(self.f)

class FODO(Map):

    def __init__(self, length, f):

        self.f = f

        RQ1 = ThinQuadrupole(2.0 * f)
        RD  = Drift(length)
        RQ2 = ThinQuadrupole(-f)

        R = RQ1 * RD * RQ2 * RD * RQ1

        super(FODO, self).__init__(R, 2*length)

    def __str__(self):
        return 'FODO(L = ' + str(self.length) \
               + ' [m], f = ' + str(self.f) + ' )\n'

    def get(self, length):
        return FODO(length, self.f)
