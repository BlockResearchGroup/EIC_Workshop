import json
import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Cylinder
from compas_viewer import Viewer

# ==============================================================================
# Define the data files
# ==============================================================================

HERE = pathlib.Path(__file__).parent
FORMFINDER = HERE / "data" / "FormFinder.json"
SESSION = HERE / "data" / "session.json"

# ==============================================================================
# Load the cablemesh
# ==============================================================================

with open(FORMFINDER) as fp:
    data = json.load(fp)
    for item in data["scene"]["data"]["items"]:
        if item["dtype"] == "compas_fofin.datastructures/CableMesh":
            cablemesh = Mesh.__from_data__(item["data"])
            break

assert cablemesh, "No CableMesh found."

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
# Preprocess
# ==============================================================================

pipes = []
for edge in cablemesh.edges():
    if cablemesh.is_edge_on_boundary(edge):
        continue

    line = cablemesh.edge_line(edge)
    radius = 0.05 * cablemesh.edge_attribute(edge, name="_f")
    pipe = Cylinder.from_line_and_radius(line, radius=radius)
    pipes.append(pipe)

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()

viewer.renderer.camera.target = [0, 0, 2]
viewer.renderer.camera.position = [3, -7, 3]

viewer.scene.add(cablemesh)
viewer.scene.add(pipes, facecolor=Color.red(), linecolor=Color.red().contrast)

viewer.show()
