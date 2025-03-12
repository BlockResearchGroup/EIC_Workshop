import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.itertools import pairwise
from compas_viewer import Viewer

# ==============================================================================
# Define the data files
# ==============================================================================

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# ==============================================================================
# Import the session
# ==============================================================================

session = compas.json_load(SESSION)

# ==============================================================================
# Load the cablemesh from the work session
# and the params
# ==============================================================================

cablemesh: Mesh = session["cablemesh"]

params = session["params"]

# ==============================================================================
# Create a thickened shell mesh
# ==============================================================================

edos: Mesh = cablemesh.copy()

for vertex in edos.vertices():
    point = cablemesh.vertex_point(vertex)
    normal = cablemesh.vertex_normal(vertex)
    newpoint = point + normal * params["thickness"]
    edos.vertex_attributes(vertex, "xyz", newpoint)

max_vertex = cablemesh._max_vertex + 1

shell: Mesh = cablemesh.copy()
shell.flip_cycles()
shell.join(edos, weld=False)

for boundary in cablemesh.vertices_on_boundaries():
    for u, v in pairwise(boundary):
        shell.add_face([v, u, u + max_vertex, v + max_vertex])

# ==============================================================================
# Project supports to plane
# ==============================================================================

for vertex in shell.vertices():
    point = shell.vertex_point(vertex)
    if point.z < 0.1:
        shell.vertex_attribute(vertex, "z", 0)

# ==============================================================================
# Add the shell to the session
# ==============================================================================

session["shell"] = shell

# ==============================================================================
# Export
# ==============================================================================

compas.json_dump(session, SESSION)

# =============================================================================
# Preprocess
# =============================================================================

normals = []
for vertex in cablemesh.vertices():
    point = cablemesh.vertex_point(vertex)
    direction = cablemesh.vertex_normal(vertex)
    normals.append(Line.from_point_direction_length(point, direction, 0.3))


# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()
viewer.renderer.camera.position = [3, -7, 3]
viewer.renderer.camera.target = [0, 0, 2]

viewer.scene.add(shell)
viewer.scene.add(normals, linecolor=Color.red(), linewidth=2, name="Normals")

viewer.show()
