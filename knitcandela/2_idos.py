import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
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
# ==============================================================================

cablemesh: Mesh = session["cablemesh"]
shell: Mesh = session["shell"]

params = session["params"]

# ==============================================================================
# Make an intrados
# ==============================================================================

idos: Mesh = cablemesh.copy()

for vertex in idos.vertices():
    point = cablemesh.vertex_point(vertex)
    normal = cablemesh.vertex_normal(vertex)
    newpoint = point + normal * (-params["shell"])
    idos.vertex_attributes(vertex, "xyz", newpoint)

# ==============================================================================
# Add the intrados to the session
# ==============================================================================

session["idos"] = idos

# ==============================================================================
# Export
# ==============================================================================

compas.json_dump(session, SESSION)

# ==============================================================================
# Preprocess
# ==============================================================================

normals = []
for vertex in idos.vertices():
    point = idos.vertex_point(vertex)
    direction = idos.vertex_normal(vertex)
    normals.append(Line.from_point_direction_length(point, direction, 0.3))

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()
viewer.renderer.camera.position = [3, -7, 3]
viewer.renderer.camera.target = [0, 0, 2]

viewer.scene.add(shell, name="Volume")
viewer.scene.add(idos, facecolor=Color.blue().lightened(50), linecolor=Color.blue(), name="Idos")
viewer.scene.add(normals, linecolor=Color.red(), linewidth=2, name="Normals")

viewer.show()
