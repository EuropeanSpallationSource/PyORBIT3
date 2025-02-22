## \namespace orbit::py_linac::lattice_modifications
## \Classes and packages of ORBIT Linac.
##

from orbit.py_linac.lattice_modifications.apertures_additions_lib import (
    GetLostDistributionArr,
)
from orbit.py_linac.lattice_modifications.apertures_additions_lib import (
    AddScrapersAperturesToLattice,
)
from orbit.py_linac.lattice_modifications.apertures_additions_lib import (
    Add_drift_apertures_to_lattice,
)
from orbit.py_linac.lattice_modifications.sns_aperture_additions import (
    AddMEBTChopperPlatesAperturesToSNS_Lattice,
)

from orbit.py_linac.lattice_modifications.apertures_additions_lib import (
    Add_quad_apertures_to_lattice,
)
from orbit.py_linac.lattice_modifications.apertures_additions_lib import (
    Add_rfgap_apertures_to_lattice,
)
from orbit.py_linac.lattice_modifications.apertures_additions_lib import (
    Add_bend_apertures_to_lattice,
)

from orbit.py_linac.lattice_modifications.rf_models_modifications_lib import (
    Replace_BaseRF_Gap_to_AxisField_Nodes,
)
from orbit.py_linac.lattice_modifications.rf_quad_overlap_modifications_lib import (
    Replace_BaseRF_Gap_and_Quads_to_Overlapping_Nodes,
)
from orbit.py_linac.lattice_modifications.quad_overlap_modifications_lib import (
    Replace_Quads_to_OverlappingQuads_Nodes,
)


# ---- modification with errors
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    ErrorForNodesModification,
)
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    CoordinateDisplacementNodesModification,
)
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    BendFieldNodesModification,
)
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    LongitudinalDisplacementNodesModification,
)
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    StraightRotationZ_NodesModification,
)
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    StraightRotationX_NodesModification,
)
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    StraightRotationY_NodesModification,
)
from orbit.py_linac.lattice_modifications.errors_modifications_lib import (
    QuadFieldsErrorsDeployment,
)


__all__ = []
__all__.append("Add_quad_apertures_to_lattice")
__all__.append("Add_bend_apertures_to_lattice")
__all__.append("Add_rfgap_apertures_to_lattice")
__all__.append("GetLostDistributionArr")
__all__.append("AddScrapersAperturesToLattice")
__all__.append("Add_drift_apertures_to_lattice")
__all__.append("AddMEBTChopperPlatesAperturesToSNS_Lattice")
__all__.append("Replace_BaseRF_Gap_to_AxisField_Nodes")
__all__.append("Replace_BaseRF_Gap_and_Quads_to_Overlapping_Nodes")
__all__.append("Replace_Quads_to_OverlappingQuads_Nodes")


__all__.append("ErrorForNodesModification")
__all__.append("CoordinateDisplacementNodesModification")
__all__.append("BendFieldNodesModification")
__all__.append("LongitudinalDisplacementNodesModification")
__all__.append("StraightRotationZ_NodesModification")
__all__.append("StraightRotationX_NodesModification")
__all__.append("StraightRotationY_NodesModification")
__all__.append("QuadFieldsErrorsDeployment")
