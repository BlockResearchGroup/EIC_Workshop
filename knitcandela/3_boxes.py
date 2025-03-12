import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import offset_polygon
from compas.itertools import pairwise
from compas_viewer import Viewer


def make_face_box_with_inset(mesh: Mesh, face: int, thickness: float, distance: float) -> Mesh:
    vertices = mesh.face_vertices(face)
    points = [vertex_point[vertex] for vertex in vertices]
    normals = [vertex_normal[vertex] for vertex in vertices]

    bottom = [Point(*point) for point in offset_polygon(points, distance=distance)]
    inset = [Point(*point) for point in offset_polygon(points, distance=distance)]
    top = [point + normal * thickness for point, normal in zip(inset, normals)]

    bottomloop = bottom + bottom[:1]
    toploop = top + top[:1]
    sides = []
    for (a, b), (aa, bb) in zip(pairwise(bottomloop[::-1]), pairwise(toploop[::-1])):
        sides.append([a, aa, bb, b])

    polygons = [bottom[::-1], top] + sides
    return Mesh.from_polygons(polygons)


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
idos: Mesh = session["idos"]

params = session["params"]

# =============================================================================
# Boxes
# =============================================================================

boxes: list[Mesh] = []

vertex_point = {vertex: idos.vertex_point(vertex) for vertex in idos.vertices()}
vertex_normal = {vertex: idos.vertex_normal(vertex) for vertex in idos.vertices()}

for face in idos.faces():
    box = make_face_box_with_inset(idos, face, params["thickness"], 0.5 * params["ribs"])
    boxes.append(box)

# ==============================================================================
# Add the boxes to the session
# ==============================================================================

session["boxes"] = boxes

# ==============================================================================
# Export
# ==============================================================================

compas.json_dump(session, SESSION)

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()
viewer.renderer.camera.position = [3, -7, 3]
viewer.renderer.camera.target = [0, 0, 2]

viewer.scene.add(shell, name="Volume")
viewer.scene.add(boxes, facecolor=Color.pink(), linecolor=Color.pink().contrast, name="Boxes")

viewer.show()
