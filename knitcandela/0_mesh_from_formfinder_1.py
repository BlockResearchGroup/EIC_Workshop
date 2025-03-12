#! python3
# venv: brg-csd
# r: compas_fofin>=0.15.2

import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Cylinder
from compas.scene import Scene

# ==============================================================================
# Define the data files
# ==============================================================================

HERE = pathlib.Path(__file__).parent
FORMFINDER = HERE / "data" / "FormFinder.json"
SESSION = HERE / "data" / "session.json"

# ==============================================================================
# Load the cablemesh
# ==============================================================================

formfinder = compas.json_load(FORMFINDER)
scene: Scene = formfinder["scene"]
meshobject = scene.find_by_name("CableMesh")

# this is a temporary hack
# it is needed because compas_fofin only registers a scene object for constraints in Rhino
# but not in any other viz context
# without converting this to a basic mesh
# loading the scene outside of Rhino will therefore throw an error
# once the data type is converted this will no longer happen
# if compas_fofin registers its scene objects properly this hack will not be necessary anymore
cablemesh = Mesh.__from_data__(meshobject.mesh.__data__)

# ==============================================================================
# Define and export a work session
# ==============================================================================

session = {
    "cablemesh": cablemesh,
    "params": {
        "thickness": 0.15,
        "ribs": 0.05,
        "shell": 0.05,
    },
}

compas.json_dump(session, SESSION)

# ==============================================================================
# Viz
# ==============================================================================

scene = Scene()
scene.clear_context()

scene.add(cablemesh)

for edge in cablemesh.edges():
    if cablemesh.is_edge_on_boundary(edge):
        continue

    line = cablemesh.edge_line(edge)
    radius = 0.05 * cablemesh.edge_attribute(edge, name="_f")
    pipe = Cylinder.from_line_and_radius(line, radius=radius)
    scene.add(pipe, color=Color.red())

scene.draw()
