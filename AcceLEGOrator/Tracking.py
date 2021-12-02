# Author:   Sichen Li
# Created:     17. November 2021
#
# This file defines the physic relations
# used in particle accelerator computations.
import numpy as np
import copy
import itertools
from numpy import linalg as la
from AcceLEGOrator.Map import Drift

class Tracking:

    def getMcell(cell):
        M_cell = cell[0]
        for M in cell[1:]:
            M_cell = M * M_cell
        return M_cell

    def _sliceMap(M, n_slice):
        if isinstance(M, Drift):
            return [M]
        else:
            L = M.length
            new_maps = []
            for i in range(n_slice):
                new_maps.append(M.get(length=L/n_slice))
            return new_maps

    def slicedCell(cell, n_slice):
        return list(itertools.chain(*[Tracking._sliceMap(M, n_slice) for M in cell]))

    def getTwissInitial(cell, axis='x'):
        M_cell = Tracking.getMcell(cell)

        # get the initial twiss parameters from 2x2 submatrix of one turn map
        __dict = {'x': 0, 'y': 2}
        M_OTM_2x2 = M_cell[__dict[axis]:__dict[axis]+2, __dict[axis]:__dict[axis]+2]
        # calculate phase advance
        mu = np.arccos(np.trace(M_OTM_2x2)/2.)
        # calculate beta, alpha
        beta = M_OTM_2x2[0,1]/np.sin(mu)
        alpha = (M_OTM_2x2[0,0]-np.cos(mu))/np.sin(mu)

        # eigenvalues, P = la.eig(M_OTM_2x2)
        # P=P/((la.det(P)*1j)**(1/len(P))) # normalize P such that la.det(P)=-1j
        # D=np.diag(eigenvalues)
        # # Compute beta and alpha
        # beta=np.real(P[0,0]**2*2)
        # alpha=-np.real(P[1,0]*np.sqrt(2*beta))
        return alpha, beta

    def getMatchedSigma(cell, ex, ey, ez=None):
        # for x plane
        ax0, bx0 = Tracking.getTwissInitial(cell, axis='x')
        gx0 = (1 + ax0**2) / bx0

        # for y plane
        ay0, by0 = Tracking.getTwissInitial(cell, axis='y')
        gy0 = (1 + ay0**2) / by0

        Jx = np.matrix([[bx0, -ax0],
                        [-ax0, gx0]]) # submatrix in x plane
        Jy = np.matrix([[by0, -ay0],
                        [-ay0, gy0]]) # submatrix in y plane

        if ez is None:
            ez = (ex+ey)/2. # just a default value

        sigma_matched = np.identity(6)
        sigma_matched[0:2, 0:2] = Jx*ex
        sigma_matched[2:4, 2:4] = Jy*ey
        sigma_matched[4:6, 4:6] = [[ez, 0],[0, ez*1e-3]] # just a default value
        return sigma_matched

    def trackBunch(bunch, cell, n_cells=1):
        pass

    def trackTwiss(cell, mu, n_cells=1, n_slice=1, twiss_init=None):
        """twiss_init: [ax0, bx0, gx0, ay0, by0, gy0] or None"""
        if twiss_init is None:
            # for x plane
            ax0, bx0 = Tracking.getTwissInitial(cell, mu, axis='x')
            gx0 = (1 + ax0**2) / bx0

            # for y plane
            ay0, by0 = Tracking.getTwissInitial(cell, mu, axis='y')
            gy0 = (1 + ay0**2) / by0

            # initial container of the twiss parameters
            twiss = [[ax0, bx0, gx0, ay0, by0, gy0]]
        else:
            # initial container of the twiss parameters
            twiss = [twiss_init]
            ax0, bx0, gx0, ay0, by0, gy0 = twiss_init

        Jx = np.matrix([[bx0, -ax0],
                        [-ax0, gx0]]) # submatrix in x plane
        Jy = np.matrix([[by0, -ay0],
                        [-ay0, gy0]]) # submatrix in y plane

        # initial container of lengths of elements
        length_till_now = 0.
        lengths = [0,]

        if n_slice > 1:
            cell = Tracking.slicedCell(cell, n_slice)
        for i in range(n_cells):
            for M in cell:
                # lengths
                length_till_now = length_till_now + M.length
                lengths.append(length_till_now)

                # propagate
                Mx = M[0:2, 0:2]
                My = M[2:4, 2:4]
                Jx = Mx * Jx * Mx.T
                Jy = My * Jy * My.T

                # extract Twiss from Jx and Jy
                # a_x, b_x, g_x,
                # a_y, b_y, g_y
                t = [-Jx[0,1], Jx[0,0], Jx[1,1],
                     -Jy[0,1], Jy[0,0], Jy[1,1]]

                # collect all twiss
                twiss = np.append(twiss, t)

        twiss = np.reshape(twiss, (len(cell)*n_cells+1, 6))
        return twiss, lengths

    def trackSigma(sigma, cell, n_cells=1, n_slice=1):
        # initial rms beam size
        sigmas = np.expand_dims(sigma, axis=0)

        length_till_now = 0.
        lengths = [0,]

        if n_slice > 1:
            cell = Tracking.slicedCell(cell, n_slice)
        for i in range(n_cells):
            for j, M in enumerate(cell):
                length_till_now = length_till_now + M.length
                lengths.append(length_till_now)
                # propagate
                sigma = M * sigma * M.T
                # append data
                sigmas = np.append(sigmas, np.expand_dims(sigma, axis=0), axis=0)
        return sigmas, lengths

    def trackDispersion(dispersion, cell, n_cells=1, n_slice=1):
        dispersion = np.matrix(dispersion).T
        dispersions = copy.deepcopy(dispersion)

        # initial container of lengths of elements
        length_till_now = 0.
        lengths = [0,]

        if n_slice > 1:
            cell = Tracking.slicedCell(cell, n_slice)
        for i in range(n_cells):
            for M in cell:
                # lengths
                length_till_now = length_till_now + M.length
                lengths.append(length_till_now)

                # extract horizontal block matrix
                M_c = np.matrix(np.zeros((3,3)))
                M_c[0:2,0:2] = M.R[0:2,0:2]
                M_c[0:2, 2] = M.R[0:2, 5]
                M_c[2,2] = 1

                # propagate dispersion
                dispersion = M_c * dispersion

                # append new values
                dispersions = np.append(dispersions, dispersion, axis=1)

        return dispersions.T, lengths
