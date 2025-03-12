#! python3
# venv: eic
# r: compas

import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import NurbsCurve
from compas.scene import Scene

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# =============================================================================
# Session Import
# =============================================================================

session = compas.json_load(SESSION)

mesh: Mesh = session["tubemesh"]
path: list[int] = session["path"]
curve: NurbsCurve = session["curve"]

# =============================================================================
# Do
# =============================================================================

# =============================================================================
# Session Export
# =============================================================================

compas.json_dump(session, SESSION)

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(mesh)
scene.add(curve)
scene.draw()
