#! python3
# venv: eic
# r: compas

import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.scene import Scene

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# =============================================================================
# Session Import
# =============================================================================

session = compas.json_load(SESSION)

# load the mesh from the session dict
mesh: Mesh = session["tubemesh"]

# =============================================================================
# Do
# =============================================================================

# retrieve all the faces where "is_selected" was changed to "True"
faces = list(mesh.faces_where(is_selected=True))

# =============================================================================
# Session Export
# =============================================================================

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(mesh, disjoint=True, show_faces=faces, show_edges=True)
scene.draw()
