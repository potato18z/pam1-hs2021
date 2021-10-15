# Author:      Matthias Frey
#              Sichen Li
# Created:     28. August 2016
# Updated:     15. October 2021

import numpy as np

from abc import abstractmethod

from AcceLEGOrator.Bunch import *

class Distribution:
    """The abstract class of distribution

    Methods
    -------
    create(N)
        the abstract method of creating N particles
    __str__()
        construct a formatted string of the distribution information
    """

    def __init__(self):
        pass


    @abstractmethod
    def create(self, N):
        pass


    @abstractmethod
    def __str__(self):
        """Construct a formatted string of the distribution information

        Returns
        -------
        info
            a string of distribution information
        """

        sign = '*' * 51
        info = sign + '\n'\
               + 'Distribution information:\n' \
               + '         Empty Distribution\n'\
               + sign
        return info


class Gaussian(Distribution):
    """A class of Gaussian distribution

    Attributes
    ----------
    __mu : array of (6,)
        mean of Gaussian distribution of the 6-vectors
    __cov : array of (6, 6)
        covariance matrix of Gaussian distribution of the 6-vectors

    Methods
    -------
    create(N)
        create N particles following the Gaussian distribution
    __str__()
        construct a formatted string of the Gaussain distribution information
    """

    def __init__(self, mu, C):
        """Define the distribution parameters

        Parameters
        ----------
        mu : array of (6,)
            mean of Gaussian distribution of the 6-vectors
        C : array of (6, 6)
            covariance matrix of Gaussian distribution of the 6-vectors
        """

        super(Gaussian, self).__init__()
        self.__mu = mu
        self.__cov = C


    def create(self, N):
        """Create N particles following the Gaussian distribution

        Parameters
        ----------
        N : int
            number of particles

        Returns
        -------
            an array of (6, N), 6-vectors of all particles
        """

        return np.random.multivariate_normal(self.__mu,
                                             self.__cov, N).T


    def __str__(self):
        """Construct a formatted string of the Gaussain distribution information

        Returns
        -------
        info
            a string of Gaussain distribution information
        """

        sign = '*' * 51
        info = sign + '\n'\
               + 'Distribution information:\n' \
               + '         Gaussian Distribution\n'\
               + '         Parameter:\n'\
               + '             * mean:\t\t' + str(self.__mu) + '\n'\
               + '             * covariance:\t' + str(self.__cov.tolist()) + '\n'\
               + sign
        return info
