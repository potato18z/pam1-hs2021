# Author:      Dr. Jochen Krempel
#              Valeria Rizzoglio
#              Dr. Andreas Adelmann
#              Matthias Frey
#              Sichen Li
# Created:     17. September 2016
# Updated:     15. October 2021
#


from scipy.constants import codata # see: http://docs.scipy.org/doc/scipy/reference/constants.html

class Constants:
    """A class of basic constants used in particle accelerator computations."""

    clight     = codata.value('speed of light in vacuum')                   # m / s
    echarge    = codata.value('elementary charge')                          # C
    pmass      = codata.value('proton mass energy equivalent in MeV')       # MeV / c^2
    emass      = codata.value('electron mass energy equivalent in MeV')     # MeV / c^2
    muon       = codata.value('muon mass energy equivalent in MeV')         # MeV / c^2
    deuteron   = codata.value('deuteron mass energy equivalent in MeV')     # MeV / c^2
    tau        = codata.value('tau mass energy equivalent in MeV')          # MeV / c^2
    triton     = codata.value('triton mass energy equivalent in MeV')       # MeV / c^2
    alpha      = codata.value('triton mass energy equivalent in MeV')       # MeV / c^2
    epsilon0   = codata.value('electric constant')                          # F m^-1
