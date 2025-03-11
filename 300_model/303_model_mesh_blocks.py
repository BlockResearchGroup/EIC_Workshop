import pathlib
import compas
from compas import json_dump
from compas.geometry import scale_vector
from compas.datastructures import Mesh
from compas_viewer.config import Config
from compas_viewer.viewer import Viewer
from compas_viewer.scene import Collection

# =============================================================================
# Load data
# =============================================================================
IFILE = pathlib.Path(__file__).parent.parent / "data" / "thrust_diagram_mesh.json"
mesh = compas.json_load(IFILE)
mesh.scale(1000)

thickness = 200
vkeys = mesh.vertex_neighbors(0, False)
edges = mesh.edge_loop([0, vkeys[0]])

for face in mesh.faces():
    face_centroid = mesh.face_centroid(face)

n_faces = mesh.number_of_faces()
ratio = n_faces / len(edges)

even_or_odd = False
grouped_faces = []
current_group = []

for i, face in enumerate(mesh.faces()):
    if i % ratio == 0:
        even_or_odd = not even_or_odd
        if len(current_group) != 0:
            grouped_faces.append(current_group)
            current_group = []

    if even_or_odd:  # Even partition: groups of two
        if len(current_group) < 2:
            current_group.append(face)
        if len(current_group) == 2:
            grouped_faces.append(current_group)
            current_group = []
    else:  # Odd partitioning: first and last are single, others are pairs
        if i % ratio == 0:
            grouped_faces.append([face])
        else:
            if len(current_group) < 2:
                current_group.append(face)
            if len(current_group) == 2:
                grouped_faces.append(current_group)
                current_group = []
if current_group:
    grouped_faces.append(current_group)


blocks = []
for group in grouped_faces:
    vertices = [
        mesh.face_vertices(group[0])[0],
        mesh.face_vertices(group[0])[1],
        mesh.face_vertices(group[-1])[2],
        mesh.face_vertices(group[-1])[3],
    ]
    mesh_v = []
    mesh_f = [
        [0, 2, 4, 6],
        [7, 5, 3, 1],
        [0, 1, 3, 2],
        [2, 3, 5, 4],
        [4, 5, 7, 6],
        [6, 7, 1, 0],
    ]
    for v in vertices:
        normal = mesh.vertex_normal(v)
        pt = mesh.vertex_point(v)
        pt_up = pt + (scale_vector(normal, thickness / 2))
        pt_down = pt + (scale_vector(normal, -thickness / 2))
        mesh_v.append(pt_up)
        mesh_v.append(pt_down)
    block = Mesh.from_vertices_and_faces(mesh_v, mesh_f)
    blocks.append(block)

# =============================================================================
# Serialize
# =============================================================================
json_dump(blocks, pathlib.Path(__file__).parent.parent / "data" / "floor_vault.json")


# =============================================================================
# Visualize
# =============================================================================
config = Config()
config.camera.target = [1500, 1000, 500]
config.camera.position = [1500, -7000, 4000]
config.camera.near = 10
config.camera.far = 100000
config.camera.pandelta = 100
config.renderer.gridsize = (20000, 20, 20000, 20)
config.renderer.show_grid = False
viewer = Viewer(config=config)
viewer.scene.add(Collection(blocks), name="floor_vault")
viewer.show()
