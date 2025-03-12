import pathlib

import compas
from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.tolerance import Tolerance
from compas_viewer import Viewer

# ==============================================================================
# Define the data files
# ==============================================================================

here = pathlib.Path(__file__).parent
sessionpath = here / "data" / "session.json"

# ==============================================================================
# Import the session
# ==============================================================================

session = compas.json_load(sessionpath)

# ==============================================================================
# Load the cablemesh from the work session
# ==============================================================================

cablemesh: Mesh = session["cablemesh"]
shell: Mesh = session["shell"]
boxes: list[Mesh] = session["boxes"]

params = session["params"]

# ==============================================================================
# Waffle
# ==============================================================================

A: Brep = Brep.from_mesh(shell)
B: list[Brep] = [Brep.from_mesh(box) for box in boxes]

waffle = A - B

filepath = here / "data" / "waffle.stp"

# ==============================================================================
# Add the waffle to the session
# ==============================================================================

# adding Breps to JSON session files currently doesn't work
# because Brep serialisation is not (fully) supported yet
# instead, we can export to the Brep to a step file

waffle.to_step(filepath)

# ==============================================================================
# Export
# ==============================================================================

# we didn't change the session
# so there is no need to export

# ==============================================================================
# Viz
# ==============================================================================

# this is a global setting
# if the linear deflection is too precise (value to small)
# conversion of breps to visualisation meshes is slow
tolerance = Tolerance()
tolerance.lineardeflection = 0.01

viewer = Viewer()
viewer.renderer.camera.position = [3, -7, 3]
viewer.renderer.camera.target = [0, 0, 2]

viewer.scene.add(waffle)
viewer.show()
