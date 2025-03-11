#! python3
# venv: brg-csd
# r: compas_rv

from pathlib import Path

import compas
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Scale

from compas.scene import Scene

# =============================================================================
# JSON file with the geometry of the model.
# =============================================================================
rhino_geometry = compas.json_load(
    Path(__file__).parent.parent / "data" / "model_input.json"
)
lines = rhino_geometry["lines"]

# =============================================================================
# RhinoVault Input
# =============================================================================
f0 = Frame([-1550, -2500, 2500], [1, 0, 0], [0, 1, 0])
f1 = Frame.worldXY()
T = Transformation.from_frame_to_frame(f0, f1)
S = Scale.from_factors([1e-3, 1e-3, 1e-3])
for key, items in rhino_geometry.items():
    for geometry in items:
        geometry.transform(S * T)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(
    rhino_geometry,
    Path(__file__).parent.parent / "data" / "model_rhino_vault_input.json",
    pretty=True,
)

# =============================================================================
# Visualize
# =============================================================================

scene = Scene()
scene.clear_context()
for mesh in rhino_geometry["meshes"]:
    scene.add(mesh)
scene.draw()
