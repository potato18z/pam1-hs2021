# Author:      Matthias Frey
#              Sichen Li
# Created:     13. October 2017
# Updated:     15. October 2021
# This file parses MAD-X file into a beamline
# composed of pyAcceLEGOrator elements.

import re

from AcceLEGOrator import *
import AcceLEGOrator.Parameter as p
from AcceLEGOrator.Particle import *

class MADXParserError(Exception):
    pass


class MADXInputError(MADXParserError):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class MADXParser:
    """A class of a simple MADX parser.
    It expects a single line per element.

    Attributes
    ----------
    __drift : dict
        the information of a drift
    __drift_pattern : str
        for printing
    __quadrupole : dict
        the information of a quadrupole
    __nQuad : int
    __quad_pattern : str
    (...doc under construction)
    """

    def __init__(self):

        self.__drift = {
            'name': '',
            'l': 0.0,
            'type': 'drift'
        }

        self.__drift_pattern = '(.*):drift,(.*)=(.*);'

        self.__quadrupole = {
            'name': '',
            'l': 0.0,
            'k1': 0.0,
            'type': 'quad'
        }

        # don't count name and type --> len - 2
        self.__nQuad = 2 * (len(self.__quadrupole) - 2)

        self.__quad_pattern = '(.*):quadrupole,(.*)=(.*),(.*)=(.*);'

        self.__dipole = {
            'name': '',
            'l': 0.0,
            'angle': 0.0,
            'k1': 0.0,
            'e1': 0.0,
            'e2': 0.0,
            'type': 'dipole'
        }

        self.__dipole_pattern = '(.*):sbend,(.*)=(.*),(.*)=(.*),(.*)=(.*),(.*)=(.*),(.*)=(.*);'

        # don't count name and type --> len - 2
        self.__nDipole = 2 * (len(self.__dipole) - 2)

        self.beam = {
            'energy': 0.0,
            'particle': ''
        }

        self.__nBeam = 2 * len(self.beam)

        self.beam_pattern = 'beam,(.*)=(.*),(.*)=(.*);'

        self.__line = {
            'name': '',
            'elem': [],
        }

        self.__line_pattern = '(.*):line=\(+(.*)\);'

        self.sequence = {
            'name':  ''
        }

        self.seq_pattern = 'use,sequence=(.*);'

        self.__elements = []
        self.__lines = []

        self.__lattice = []


    def parse(self, fn):
        """
        fn (str)    filename

        """

        nLine = 0
        with open(fn, 'r') as f:
            for line in f:
                nLine += 1
                line = self._noWhitespace(line)

                if line[0] == '!':
                    # this is a comment
                    pass
                elif 'drift' in line:

                    obj = re.match(self.__drift_pattern, line)

                    # first tag is name
                    self.__drift['name'] = obj.group(1)

                    if obj.group(2) in self.__drift:
                        self.__drift[obj.group(2)] = float(obj.group(3))
                    else:
                        raise MADXInputError('Drift',
                                             'Line ' + str(nLine) + ': Parameter ' + "'" + obj.group(2) + "'" +
                                              ' does not exist for drift.')

                    self.__elements.append( self.__drift.copy() )

                elif 'quadrupole' in line:

                    obj = re.match(self.__quad_pattern, line)

                    # first tag is name
                    self.__quadrupole['name'] = obj.group(1)

                    for i in range(2, self.__nQuad+2, 2):
                        if obj.group(i) in self.__quadrupole:
                            self.__quadrupole[obj.group(i)] = float(obj.group(i+1))
                        else:
                            raise MADXInputError('Quadrupole',
                                                 'Line ' + str(nLine) + ': Parameter ' + "'" + obj.group(i) + "'" +
                                                 ' does not exist for quadrupole.')

                    self.__elements.append( self.__quadrupole.copy() )

                elif 'sbend' in line:

                    obj = re.match(self.__dipole_pattern, line)

                    # first tag is name
                    self.__dipole['name'] = obj.group(1)

                    for i in range(2, self.__nDipole + 2, 2):

                        if obj.group(i) in self.__dipole:
                            self.__dipole[obj.group(i)] = float(obj.group(i+1))
                        else:
                            raise MADXInputError('Dipole',
                                                 'Line ' + str(nLine) + ': Parameter ' +
                                                 "'" + obj.group(i) + "'" +
                                                 ' does not exist for dipole.')

                    self.__elements.append( self.__dipole.copy() )
                elif 'marker' in line:
                    pass

                elif 'beam' in line:

                    obj = re.match(self.beam_pattern, line)

                    for i in range(1, self.__nBeam, 2):
                        if obj.group(i) in self.beam:
                            if obj.group(i+1).isdigit():
                                self.beam[obj.group(i)] = float(obj.group(i+1))
                            else:
                                self.beam[obj.group(i)] = obj.group(i+1)

                        else:
                            raise MADXInputError('Beam',
                                                 'Line ' + str(nLine) + ': Parameter ' +
                                                 "'" + obj.group(i) + "'" +
                                                 ' does not exist for beam.')

                elif 'line' in line:

                    obj = re.match(self.__line_pattern, line)

                    self.__line['name'] = obj.group(1)

                    lines = obj.group(2).split(',')
                    newlines = []

                    # check multiplication and insert that many lines
                    for l in lines:
                        if '*' in l:
                            tmp = l.split('*')

                            n = 0
                            ll = ''

                            if tmp[0].isdigit():
                                n = int(tmp[0])
                                ll = tmp[1]
                            else:
                                n = int(tmp[1])
                                ll = tmp[0]

                            newlines += [ll] * n

                        else:
                            newlines.append(l)

                    self.__line['elem'] = newlines

                    self.__lines.append( self.__line.copy() )

                elif 'use' in line and 'sequence' in line:

                    obj = re.match(self.seq_pattern, line)

                    self.sequence['name'] = obj.group(1)
                else:
                    raise MADXInputError('', 'Error at line ' + str(nLine))


        # 14. Oct. 2017,
        # https://stackoverflow.com/questions/7900882/extract-item-from-list-of-dictionaries
        start = [l for l in self.__lines if l['name'] == self.sequence['name']][0]

        self._flatten(start)

        # we need to add start line
        self.__lattice = [start] + self.__lattice

        self.__lattice = self._combine(self.__lattice)


    def _flatten(self, line):
        """
        Find sublines.

        """

        name = line['name']

        for l in self.__lines:
            if name in l['name']:
                for ll in l['elem']:
                    for lll in self.__lines:
                        if lll['name'] == ll:
                            self.__lattice.append(lll)
                            self._flatten(lll)


    def _combine(self, lattice):
        """
        Combine to one list of all basic
        elements.

        return a list of of element dictionaries
        """


        l1 = self.__lattice[0]

        for i in range(1, len(self.__lattice)):
            l2 = self.__lattice[i]

            for e in l1['elem']:
                if l2['name'] == e:
                    idx = l1['elem'].index(e)
                    l1['elem'].remove(e)
                    l1['elem'] = l1['elem'][0:idx] + l2['elem'] + l1['elem'][idx:]

        return l1


    def _noWhitespace(self, string):
        """
        Remove white space from a string.

        14. Oct. 2017,
        https://stackoverflow.com/questions/3739909/how-to-strip-all-whitespace-from-string

        """
        return string.replace(' ', '')


    def __str__(self):

        if self.__lattice:
            length = 0.0

            # drift, dipole, quadrupole
            nTypes = [0, 0, 0]

            for elem in self.__lattice['elem']:
                for e in self.__elements:
                    if elem == e['name']:
                        length += e['l']

                        if e['type'] == 'drift':
                            nTypes[0] += 1
                        elif e['type'] == 'dipole':
                            nTypes[1] += 1
                        elif e['type'] == 'quad':
                            nTypes[2] += 1
                        break

            sign = '*' * 70
            info = sign + '\n'\
                + 'MADX-Parser information:\n' \
                + '         length:\t' + str(length) + ' [m]\n'\
                + '      #elements:\t' + str(len(self.__lattice['elem'])) + '\n'\
                + '            *       #drift:\t' + str(nTypes[0]) + '\n'\
                + '            *      #dipole:\t' + str(nTypes[1]) + '\n'\
                + '            *  #quadrupole:\t' + str(nTypes[2]) + '\n'\
                + '           beam:\t\n'\
                + '            *     particle:\t' + self.beam['particle'] + '\n'\
                + '            * total energy:\t' + str(self.beam['energy']) + ' [GeV]\n'\
                + sign

            return info
        else:
            return 'No information available.'

    def getBeamline(self):
        if self.__lattice:

            particle = self.getParticle()

            epot = particle.mass
            p.ekin = self.beam['energy'] * 1.0e3 - epot  # MeV

            # set gamma and kinetic energy
            # in order to build maps
            p.gamma_0 = Physics.getGamma(p.ekin, epot)
            p.mass    = particle.mass
            p.charge  = particle.charge

            c  = Constants.clight
            beta_0 = Physics.getBeta(p.gamma_0)
            p0 = p.mass * 1e6 / c * p.gamma_0 * beta_0

            beamline = []

            for elem in self.__lattice['elem']:
                for e in self.__elements:
                    if elem == e['name']:
                        if e['type'] == 'drift':
                            beamline.append(Drift(e['l']))
                        elif e['type'] == 'dipole':

                            # compute magnetic field strength
                            # using beam rigidity
                            r = e['l'] / e['angle']
                            B = p0 / ( p.charge * r )

                            beamline.append(Dipole(e['l'], B, 0, 0))
                        elif e['type'] == 'quad':
                            # compute gradient
                            gradB = p0 * e['k1'] / p.charge

                            beamline.append(Quadrupole(e['l'], gradB, 0.0))
                        else:
                            print ( 'Skipping element type ' + "'" +
                                    e['type'] + "'" )
            return beamline

        else:
            return []


    def getParticle(self):
        particle = None
        if self.beam['particle'] == 'electron':
            particle = Electron()
        elif self.beam['particle'] == 'proton':
            particle = Proton()
        else:
            raise MADXInputError('', 'No particle type ' + "'" +
                                 self.beam['particle'] + "' available.")

        return particle


    def getEtot(self):
        return self.beam['energy']
