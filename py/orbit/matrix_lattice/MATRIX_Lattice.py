"""
The general Matrix lattice. The matrices track the bunch as
the linear transport elements. It is a base class for TEAPOT_MATRIX_Lattice,
but it can be used by itself if user specifies the transport matrices by using
addNode(BaseMATRIX). After adding nodes the user has to initialize() the lattice.
The initialization will create one turn matrix, but the user can ignore it if
the lattice is a linac lattice.
The  This class cannot calculate chromaticities.
"""

import os
import math


# import bunch
from orbit.core.bunch import Bunch

# import the function that creates multidimensional arrays
from ..utils import orbitFinalize

# import general accelerator elements and lattice
from ..lattice import AccLattice, AccNode, AccActionsContainer, AccNodeBunchTracker

# import matrix class and generators
from ..teapot_base import MatrixGenerator
from orbit.core.orbit_utils import Matrix, PhaseVector

# import the AccNode implementation for a transport matrix
from .BaseMATRIX import BaseMATRIX


class MATRIX_Lattice(AccLattice):
    """
    The subclass of the AccLattice class. Shell class for the BaseMATRIX nodes collection.
    In the beginning the lattcie is empty.
    """

    def __init__(self, name=None):
        AccLattice.__init__(self, name)
        self.oneTurnMatrix = Matrix(7, 7)
        self.oneTurnMatrix.unit()

        self.Matrix = Matrix(7, 7)
        self.Matrix.unit()

    def initialize(self):
        """
        Method. Initializes the matrix lattice, child node structures, and calculates
        the one turn matrix.
        """
        AccLattice.initialize(self)
        self.makeOneTurnMatrix()

    def makeOneTurnMatrix(self):
        """
        Calculates the one turn matrix.
        """
        self.oneTurnMatrix.unit()
        eps_length = 0.00001  # 10^-6 meter

        position = 0.0
        position_old = position
        for matrixNode in self.getNodes():
            if isinstance(matrixNode, BaseMATRIX) == True:
                self.oneTurnMatrix = matrixNode.getMatrix().mult(self.oneTurnMatrix)
                """
				if(abs(position_old-position) > eps_length):
					print position, self.oneTurnMatrix.get(0,6)
				position_old = position
				position = position + matrixNode.getLength()
				"""
        return self.oneTurnMatrix

    def makeMatrix(self, pos):
        """
        Calculates the one turn matrix.
        """
        self.Matrix.unit()
        position = 0.0
        for matrixNode in self.getNodes():
            if isinstance(matrixNode, BaseMATRIX) == True and position < pos:
                self.Matrix = matrixNode.getMatrix().mult(self.Matrix)
                position = position + matrixNode.getLength()
                # print position, self.Matrix.get(0,6)
        return self.Matrix

    def getOneTurnMatrix(self):
        """
        Returns the one turn matrix.
        """
        return self.oneTurnMatrix

    def getRingParametersDict(self, momentum, mass):
        """
        Returns the dictionary with different ring parametrs
        calculated from the one turn transport matrix.
        """
        res_dict = {}
        Etotal = math.sqrt(momentum**2 + mass**2)
        beta = momentum / Etotal
        gamma = Etotal / mass
        Ekin = Etotal - mass
        res_dict["momentum [GeV/c]"] = momentum
        res_dict["mass [GeV]"] = mass
        res_dict["Ekin [GeV]"] = Ekin
        # longitudinal params
        c = 2.99792458e8
        ring_length = self.getLength()
        T = ring_length / (beta * c)
        res_dict["period [sec]"] = T
        res_dict["frequency [Hz]"] = 1.0 / T
        # transverse twiss parameters
        mt = self.oneTurnMatrix
        res_dict["fractional tune x"] = None
        res_dict["fractional tune y"] = None
        res_dict["alpha x"] = None
        res_dict["alpha y"] = None
        res_dict["beta x [m]"] = None
        res_dict["beta y [m]"] = None
        res_dict["gamma x [m^-1]"] = None
        res_dict["gamma y [m^-1]"] = None
        res_dict["dispersion x [m]"] = None
        res_dict["dispersion y [m]"] = None
        res_dict["dispersion prime x"] = None
        res_dict["dispersion prime y"] = None
        cos_phi_x = (mt.get(0, 0) + mt.get(1, 1)) / 2.0
        cos_phi_y = (mt.get(2, 2) + mt.get(3, 3)) / 2.0
        if abs(cos_phi_x) >= 1.0 or abs(cos_phi_y) >= 1.0:
            return res_dict
        sign_x = +1.0
        if abs(mt.get(0, 1)) != 0.0:
            sign_x = mt.get(0, 1) / abs(mt.get(0, 1))
        sign_y = +1.0
        if abs(mt.get(2, 3)) != 0.0:
            sign_y = mt.get(2, 3) / abs(mt.get(2, 3))
        sin_phi_x = math.sqrt(1.0 - cos_phi_x * cos_phi_x) * sign_x
        sin_phi_y = math.sqrt(1.0 - cos_phi_y * cos_phi_y) * sign_y
        nux = math.acos(cos_phi_x) / (2 * math.pi) * sign_x
        nuy = math.acos(cos_phi_y) / (2 * math.pi) * sign_y
        res_dict["fractional tune x"] = nux
        res_dict["fractional tune y"] = nuy
        # alpha, beta, gamma
        beta_x = mt.get(0, 1) / sin_phi_x
        beta_y = mt.get(2, 3) / sin_phi_y
        alpha_x = (mt.get(0, 0) - mt.get(1, 1)) / (2 * sin_phi_x)
        alpha_y = (mt.get(2, 2) - mt.get(3, 3)) / (2 * sin_phi_y)
        gamma_x = -mt.get(1, 0) / sin_phi_x
        gamma_y = -mt.get(3, 2) / sin_phi_y
        # dispersion and dispersion prime
        m_coeff = momentum * momentum / Etotal
        disp_x = m_coeff * (mt.get(0, 5) * (1 - mt.get(1, 1)) + mt.get(0, 1) * mt.get(1, 5)) / (2 - mt.get(0, 0) - mt.get(1, 1))
        disp_y = m_coeff * (mt.get(2, 5) * (1 - mt.get(3, 3)) + mt.get(2, 3) * mt.get(3, 5)) / (2 - mt.get(2, 2) - mt.get(3, 3))
        disp_pr_x = m_coeff * (mt.get(1, 0) * mt.get(0, 5) + mt.get(1, 5) * (1 - mt.get(0, 0))) / (2 - mt.get(0, 0) - mt.get(1, 1))
        disp_pr_y = m_coeff * (mt.get(3, 2) * mt.get(2, 5) + mt.get(3, 5) * (1 - mt.get(2, 2))) / (2 - mt.get(2, 2) - mt.get(3, 3))
        res_dict["alpha x"] = alpha_x
        res_dict["alpha y"] = alpha_y
        res_dict["beta x [m]"] = beta_x
        res_dict["beta y [m]"] = beta_y
        res_dict["gamma x [m^-1]"] = gamma_x
        res_dict["gamma y [m^-1]"] = gamma_y
        res_dict["dispersion x [m]"] = disp_x
        res_dict["dispersion y [m]"] = disp_y
        res_dict["dispersion prime x"] = disp_pr_x
        res_dict["dispersion prime y"] = disp_pr_y
        # more longitudinal params
        termx = mt.get(4, 0) * disp_x
        termxp = mt.get(4, 1) * disp_pr_x
        termy = mt.get(4, 2) * disp_y
        termyp = mt.get(4, 3) * disp_pr_y
        termdE = mt.get(4, 5) * beta * beta * Etotal
        eta_ring = -(termx + termxp + termy + termyp + termdE) / ring_length
        res_dict["eta"] = eta_ring
        alpha_p = eta_ring + 1.0 / (gamma * gamma)
        sqarg = alpha_p
        if alpha_p < 0.0:
            sqarg = -alpha_p
        gamma_trans = 1.0 / math.sqrt(sqarg)
        res_dict["gamma transition"] = gamma_trans
        res_dict["transition energy [GeV]"] = (gamma_trans - 1.0) * mass
        res_dict["momentum compaction"] = alpha_p
        return res_dict

    def getRingTwissDataX(self, momentum, mass):
        """
        Returns the tuple ([(position, phase advanceX)/2/pi,...],[(position, alphaX),...],[(position,betaX),...] ).
        """
        res_dict = self.getRingParametersDict(momentum, mass)
        alpha_x = res_dict["alpha x"]
        beta_x = res_dict["beta x [m]"]
        return self.trackTwissData(alpha_x, beta_x, "x")

    def getRingTwissDataY(self, momentum, mass):
        """
        Returns the tuple ([(position, phase advanceY/2/pi),...],[(position, alphaY),...],[(position,betaY),...] ).
        """
        res_dict = self.getRingParametersDict(momentum, mass)
        alpha_y = res_dict["alpha y"]
        beta_y = res_dict["beta y [m]"]
        return self.trackTwissData(alpha_y, beta_y, "y")

    def trackTwissData(self, alpha, beta, direction="x"):
        """
        Returns the tuple ([(position, phase advance/2/pi),...], [(position, alpha),...],[(position,beta),...] ).
        The tracking starts from the values specified as the initial parameters.
        The possible values for direction parameter "x" or "y".
        """
        if direction.lower() != "x" and direction.lower() != "y":
            orbitFinalize("Class orbit.matrix_lattice.MATRIX_Lattice, method trackTwissData(...): direction should be x or y.")
        # track twiss
        eps_length = 0.00001  # 10^-6 meter
        dir_ind = 0
        if direction.lower() == "y":
            dir_ind = 2
        gamma = (1.0 + alpha * alpha) / beta
        track_m = Matrix(3, 3)
        track_m.unit()
        track_v = PhaseVector(3)
        track_v.set(0, alpha)
        track_v.set(1, beta)
        track_v.set(2, gamma)
        position = 0.0
        pos_arr = []
        alpha_arr = []
        beta_arr = []
        # phi is for tune accumulation
        phi = 0.0
        # phase advance
        mu_arr = []
        # count = 0
        pos_arr.append(position)
        mu_arr.append(phi)
        alpha_arr.append(track_v.get(0))
        beta_arr.append(track_v.get(1))
        for matrixNode in self.getNodes():
            if isinstance(matrixNode, BaseMATRIX) == True:
                # only the main nodes are used, the or-cases deal with markers with zero length
                mt = matrixNode.getMatrix()
                ind0 = 0 + dir_ind
                ind1 = 1 + dir_ind
                track_m.set(
                    0,
                    0,
                    mt.get(ind0, ind0) * mt.get(ind1, ind1) + mt.get(ind0, ind1) * mt.get(ind1, ind0),
                )
                track_m.set(0, 1, -mt.get(ind0, ind0) * mt.get(ind1, ind0))
                track_m.set(0, 2, -mt.get(ind0, ind1) * mt.get(ind1, ind1))
                track_m.set(1, 0, -2 * mt.get(ind0, ind0) * mt.get(ind0, ind1))
                track_m.set(1, 1, mt.get(ind0, ind0) * mt.get(ind0, ind0))
                track_m.set(1, 2, mt.get(ind0, ind1) * mt.get(ind0, ind1))
                track_m.set(2, 0, -2 * mt.get(ind1, ind0) * mt.get(ind1, ind1))
                track_m.set(2, 1, mt.get(ind1, ind0) * mt.get(ind1, ind0))
                track_m.set(2, 2, mt.get(ind1, ind1) * mt.get(ind1, ind1))
                alpha_0 = track_v.get(0)
                beta_0 = track_v.get(1)
                delta_phi = math.atan(mt.get(ind0, ind1) / (beta_0 * mt.get(ind0, ind0) - alpha_0 * mt.get(ind0, ind1)))
                phi = phi + delta_phi
                track_v = track_m.mult(track_v)
                position = position + matrixNode.getLength()
                # print position, matrixNode.getParam("matrix_parent_node_active_index") == 1
                # print position, matrixNode.getName(), track_v.get(1)

                if matrixNode.getLength() > 0:
                    # print position, matrixNode.getName(), track_v.get(1)
                    pos_arr.append(position)
                    alpha_arr.append(track_v.get(0))
                    beta_arr.append(track_v.get(1))
                    mu_arr.append(phi / (2 * math.pi))
            # count = count + 1
        # pack the resulting tuple
        tune = phi / (2 * math.pi)
        graph_alpha_arr = []
        graph_beta_arr = []
        graph_mu_arr = []
        # print count, len(pos_arr)
        for i in range(len(pos_arr)):
            graph_mu_arr.append((pos_arr[i], mu_arr[i]))
            graph_alpha_arr.append((pos_arr[i], alpha_arr[i]))
            graph_beta_arr.append((pos_arr[i], beta_arr[i]))
        return (graph_mu_arr, graph_alpha_arr, graph_beta_arr)

    def getRingDispersionDataX(self, momentum, mass):
        """
        Returns the tuple  ([(position, dispX),...],[(position,disp_pX),...] ).
        """
        res_dict = self.getRingParametersDict(momentum, mass)
        disp = res_dict["dispersion x [m]"]
        disp_p = res_dict["dispersion prime x"]
        return self.trackDispersionData(momentum, mass, disp, disp_p, "x")

    def getRingDispersionDataY(self, momentum, mass):
        """
        Returns the tuple  ([(position, dispY),...],[(position,disp_pY),...] ).
        """
        res_dict = self.getRingParametersDict(momentum, mass)
        disp = res_dict["dispersion y [m]"]
        disp_p = res_dict["dispersion prime y"]
        return self.trackDispersionData(momentum, mass, disp, disp_p, "y")

    def trackDispersionData(self, momentum, mass, disp, disp_p, direction="x"):
        """
        Returns the tuple ([(position, disp),...],[(position,disp_p),...] ).
        The tracking starts from the values specified as the initial parameters.
        The possible values for direction parameter "x" or "y".
        """
        if direction.lower() != "x" and direction.lower() != "y":
            orbitFinalize("Class orbit.matrix_lattice.MATRIX_Lattice, method trackDispersionData(...): direction should be x or y.")
        # track dispersion
        eps_length = 0.00001  # 10^-6 meter
        dir_ind = 0
        if direction.lower() == "y":
            dir_ind = 2
        track_m = Matrix(3, 3)
        track_m.unit()
        track_m.set(2, 0, 0.0)
        track_m.set(2, 1, 0.0)
        track_m.set(2, 2, 1.0)
        track_v = PhaseVector(3)
        # kinematics coefficient calculation
        Etotal = math.sqrt(momentum**2 + mass**2)
        beta = momentum / Etotal
        gamma = Etotal / mass
        Ekin = Etotal - mass
        m_coeff = momentum * momentum / (mass + Ekin)
        track_v.set(0, disp)
        track_v.set(1, disp_p)
        track_v.set(2, 1.0)
        position = 0.0
        pos_arr = []
        disp_arr = []
        disp_p_arr = []
        # put in array the initial dispersions
        # count = 0
        pos_arr.append(position)
        disp_arr.append(track_v.get(0))
        disp_p_arr.append(track_v.get(1))
        for matrixNode in self.getNodes():
            if isinstance(matrixNode, BaseMATRIX) == True:
                mt = matrixNode.getMatrix()
                ind0 = 0 + dir_ind
                ind1 = 1 + dir_ind
                track_m.set(0, 0, mt.get(ind0, ind0))
                track_m.set(0, 1, mt.get(ind0, ind1))
                track_m.set(1, 0, mt.get(ind1, ind0))
                track_m.set(1, 1, mt.get(ind1, ind1))
                track_m.set(0, 2, mt.get(ind0, 5) * m_coeff)
                track_m.set(1, 2, mt.get(ind1, 5) * m_coeff)
                track_v = track_m.mult(track_v)
                position = position + matrixNode.getLength()
                # only the main nodes are used, the or-cases deal with markers with zero length
                if isinstance(matrixNode, BaseMATRIX) == True:
                    pos_arr.append(position)
                    disp_arr.append(track_v.get(0))
                    disp_p_arr.append(track_v.get(1))
        # pack the resulting tuple
        graph_disp_arr = []
        graph_disp_p_arr = []
        for i in range(len(pos_arr)):
            graph_disp_arr.append((pos_arr[i], disp_arr[i]))
            graph_disp_p_arr.append((pos_arr[i], disp_p_arr[i]))
        return (graph_disp_arr, graph_disp_p_arr)

    def getRingOrbit(self, z0):
        """
        Returns the tuple ([(position, x] ).
        """
        return self.trackOrbit(z0)

    def trackOrbit(self, z0):
        """
        Returns the tuple ([(position, x),...], [(position, y),...] ).
        The tracking starts from the values specified as the initial parameters.
        z0 fulfill: z0 = Mz0 with M as one turn matrix
        """

        eps_length = 0.00001  # 10^-6 meter

        pos_arr = []
        orbitX_arr = []
        orbitY_arr = []
        orbitXP_arr = []
        orbitYP_arr = []

        position = 0.0
        pos_arr.append(position)

        track_o = Matrix(6, 6)

        track_ov = PhaseVector(6)
        track_ov.set(0, z0[0])
        track_ov.set(1, z0[1])
        track_ov.set(2, z0[2])
        track_ov.set(3, z0[3])
        track_ov.set(4, z0[4])
        track_ov.set(5, z0[5])

        orbitX_arr.append(track_ov.get(0))
        orbitY_arr.append(track_ov.get(2))
        orbitXP_arr.append(track_ov.get(1))
        orbitYP_arr.append(track_ov.get(3))

        position_old = position

        for matrixNode in self.getNodes():
            if isinstance(matrixNode, BaseMATRIX) == True:
                if abs(position_old - position) > eps_length:
                    pos_arr.append(position)
                    orbitX_arr.append(track_ov.get(0))
                    orbitY_arr.append(track_ov.get(2))
                    orbitXP_arr.append(track_ov.get(1))
                    orbitYP_arr.append(track_ov.get(3))

                mt = matrixNode.getMatrix()

                for i in range(6):
                    for j in range(6):
                        track_o.set(i, j, mt.get(i, j))
                track_ov = track_o.mult(track_ov)

                for i in range(6):
                    tmp = track_ov.get(i)
                    track_ov.set(i, tmp + mt.get(i, 6))

                position_old = position
                position = position + matrixNode.getLength()

        pos_arr.append(position)
        orbitX_arr.append(track_ov.get(0))
        orbitY_arr.append(track_ov.get(2))
        orbitXP_arr.append(track_ov.get(1))
        orbitYP_arr.append(track_ov.get(3))
        # pack the resulting tuple
        graph_orbitX_arr = []
        graph_orbitY_arr = []
        for i in range(len(pos_arr)):
            graph_orbitX_arr.append((pos_arr[i], orbitX_arr[i], orbitXP_arr[i]))
            graph_orbitY_arr.append((pos_arr[i], orbitY_arr[i], orbitYP_arr[i]))

        return (graph_orbitX_arr, graph_orbitY_arr)

    def getSubLattice(
        self,
        index_start=-1,
        index_stop=-1,
    ):
        """
        It returns the new MATRIX_Lattice with children with indexes
        between index_start and index_stop inclusive
        """
        return self._getSubLattice(MATRIX_Lattice(), index_start, index_stop)

    def trackBunch(self, bunch, paramsDict={}, actionContainer=None):
        """
        It tracks the bunch through the lattice.
        """
        if actionContainer == None:
            actionContainer = AccActionsContainer("Bunch Tracking")
        paramsDict["bunch"] = bunch

        def track(paramsDict):
            node = paramsDict["node"]
            node.track(paramsDict)

        actionContainer.addAction(track, AccActionsContainer.BODY)
        self.trackActions(actionContainer, paramsDict)
        actionContainer.removeAction(track, AccActionsContainer.BODY)
