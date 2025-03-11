from pathlib import Path

import compas
from compas import json_dump
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import bounding_box
from compas.geometry import Scale
from compas_grid.elements import BeamElement
from compas_viewer import Viewer
from compas_viewer.config import Config
from compas_model.models import Model


# =============================================================================
# Load Model
# =============================================================================

model: Model = compas.json_load(
    Path(__file__).parent.parent / "data" / "model_with_modifiers.json"
)

# =============================================================================
# Convert element to convex meshes in meters.
# =============================================================================

elements = list(model.elements())
meshes_to_serialize = []
S = Scale.from_factors([1e-3, 1e-3, 1e-3])
for element in elements:
    if isinstance(element, BeamElement):
        mesh = element.elementgeometry
        V = list(mesh.vertices())
        points1 = [mesh.vertex_point(V[0]), mesh.vertex_point(V[10])]
        points2 = [mesh.vertex_point(V[6]), mesh.vertex_point(V[12])]
        box1 = Mesh.from_shape(Box.from_bounding_box(bounding_box(points1)))
        box2 = Mesh.from_shape(Box.from_bounding_box(bounding_box(points2)))
        box1.transform(S * element.transformation)
        box2.transform(S * element.transformation)
        box1.name = element.name
        box2.name = element.name
        meshes_to_serialize.append([box1, box2])
    else:
        mesh = element.modelgeometry
        mesh.name = element.name
        mesh.transform(S)
        meshes_to_serialize.append([mesh])

# =============================================================================
# Serialize
# =============================================================================

json_dump(
    meshes_to_serialize,
    Path(__file__).parent.parent / "data" / "model_for_structural_analysis.json",
)

# =============================================================================
# Visualize
# =============================================================================
config = Config()
config.renderer.show_grid = False
viewer = Viewer(config=config)

for meshes in meshes_to_serialize:
    viewer.scene.add(meshes)

viewer.show()
