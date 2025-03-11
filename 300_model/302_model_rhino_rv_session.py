#! python3
# venv: brg-csd
# r: compas_rv

import pathlib
import compas
from compas.datastructures import Mesh
from compas.scene import Scene
from compas_tna.diagrams import FormDiagram
from compas import json_dump


# =============================================================================
# Load data
# =============================================================================
IFILE = (
    pathlib.Path(__file__).parent.parent
    / "data"
    / "RhinoVAULT_Barrel_vertical_equ.json"
)
print(IFILE)

rv_session = compas.json_load(IFILE)
rv_scene: Scene = rv_session["scene"]

thrustobject = rv_scene.find_by_name("ThrustDiagram")
thrustdiagram: FormDiagram = thrustobject.mesh

mesh: Mesh = thrustdiagram.copy(cls=Mesh)

for face in list(mesh.faces_where(_is_loaded=False)):
    mesh.delete_face(face)


# =============================================================================
# Serialize
# =============================================================================
json_dump(
    mesh, pathlib.Path(__file__).parent.parent / "data" / "thrust_diagram_mesh.json"
)

# =============================================================================
# Visualize
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(mesh)
scene.draw()
