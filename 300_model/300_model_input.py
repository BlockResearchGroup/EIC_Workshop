from pathlib import Path

import compas
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# Create Geometry in MM
# =============================================================================

points = [
    Point(-1550, -2500, 0),
    Point(-1550, 2500, 0),
    Point(1550, 2500, 0),
    Point(1550, -2500, 0),
    Point(-1550, -2500, 3800),
    Point(-1550, 2500, 3800),
    Point(1550, 2500, 3800),
    Point(1550, -2500, 3800),
]

lines = [
    Line(points[0], points[4]),
    Line(points[1], points[5]),
    Line(points[2], points[6]),
    Line(points[3], points[7]),
    Line(points[4], points[5]),
    Line(points[6], points[7]),
    Line(points[5], points[6]),
    Line(points[7], points[4]),
]

mesh = Mesh.from_vertices_and_faces(points[4:], [[0, 1, 2, 3]])

# =============================================================================
# Serialize the Frame into a JSON file.
# =============================================================================

model_input = {"lines": lines, "meshes": [mesh]}

compas.json_dump(
    model_input, Path(__file__).parent.parent / "data" / "model_input.json", pretty=True
)

# =============================================================================
# Visualize
# =============================================================================

config = Config()
config.camera.target = [0, 1000, 1250]
config.camera.position = [0, -10000, 8125]
config.camera.near = 10
config.camera.far = 100000
config.camera.pandelta = 100
config.renderer.gridsize = (20000, 20, 20000, 20)
config.renderer.show_grid = False
viewer = Viewer(config=config)
viewer.scene.add(lines, linewidth=3, name="lines")
viewer.scene.add(mesh, name="floor")

viewer.show()
