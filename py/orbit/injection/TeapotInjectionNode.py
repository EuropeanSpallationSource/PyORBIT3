"""
This module is a foil node class for TEAPOT lattice
"""

import os
import math

# import the auxiliary classes
from ..utils import orbitFinalize, NamedObject, ParamsDictObject

# import general accelerator elements and lattice
from ..lattice import AccNode, AccActionsContainer, AccNodeBunchTracker

# import teapot drift class
from ..teapot import DriftTEAPOT

# import injection class
from . import InjectParts


class TeapotInjectionNode(DriftTEAPOT):
    """
    The injection node class for TEAPOT lattice
    """

    def __init__(
        self,
        nparts,
        bunch,
        lostbunch,
        foilparams,
        xDistFunc,
        yDistFunc,
        lDistFun,
        nmaxmacroparticles=-1,
        name="injection",
    ):
        """
        Constructor. Creates the Injection TEAPOT element.
        """
        DriftTEAPOT.__init__(self, name)
        self.injectparts = InjectParts(
            nparts,
            bunch,
            lostbunch,
            foilparams,
            xDistFunc,
            yDistFunc,
            lDistFun,
            nmaxmacroparticles,
        )
        self.setType("Injection")
        self.setLength(0.0)

    def track(self, paramsDict):
        """
        The injection-teapot class implementation of the AccNodeBunchTracker class track(probe) method.
        """
        self.injectparts.addParticles()

    def setnparts(self, nparts):
        self.injectparts.setnparts(nparts)
