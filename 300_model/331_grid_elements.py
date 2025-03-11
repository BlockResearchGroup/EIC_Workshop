from pathlib import Path

import compas
from compas_grid.models import GridModel
from compas_grid.elements import BeamProfileElement
from compas_grid.elements import BlockElement
from compas_grid.elements import ColumnElement
from compas.geometry import Translation
from compas.geometry import Scale
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# JSON file with the geometry of the model.
# =============================================================================

rhino_geometry = compas.json_load(
    Path(__file__).parent.parent / "data" / "model_input_grid.json"
)
lines = rhino_geometry["lines"]
meshes = rhino_geometry["meshes"]

# =============================================================================
# Model
# =============================================================================

model = GridModel.from_lines_and_surfaces(
    columns_and_beams=lines, floor_surfaces=meshes
)

edges_columns = list(
    model.cell_network.edges_where({"is_column": True})
)  # Order as in the model
edges_beams = list(
    model.cell_network.edges_where({"is_beam": True})
)  # Order as in the model
faces_floors = list(
    model.cell_network.faces_where({"is_floor": True})
)  # Order as in the model

# =============================================================================
# Add Column on a CellNetwork Edge
# =============================================================================

for edge in edges_columns:
    column = ColumnElement(300, 300)
    model.add_column(column, edge)

# =============================================================================
# Add Beams on a CellNetwork Edge
# =============================================================================

for edge_index in [0, 3, 6, 9]:
    height = 700
    beam = BeamProfileElement.from_t_profile(
        width=300, height=height, step_width_left=75, step_height_left=120
    )
    beam.transform = Translation.from_vector([0, 0, beam.height * 0.5])
    model.add_beam(beam, edges_beams[edge_index], 150)

# =============================================================================
# Add Plates on a CellNetwork Face
# Add model to the plate of the grid model
# =============================================================================

barrel_vault_meshes = compas.json_load(
    Path(__file__).parent.parent / "data" / "floor_vault.json"
)
for idx, face in enumerate(faces_floors):
    for mesh in barrel_vault_meshes:
        block = BlockElement(shape=mesh)
        block.is_support = mesh.aabb().frame.point[2] < 25
        S = Scale.from_factors([1, 1, 1])

        T = Translation.from_vector([-1500 + idx * 3100, -2500, 4000])
        block.transformation = T * S
        model.add_element(block)

# =============================================================================
# Process elements
# =============================================================================
elements = list(model.elements())
columns = [element for element in elements if isinstance(element, ColumnElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
blocks = [element for element in elements if isinstance(element, BlockElement)]

# =============================================================================
# Export
# =============================================================================

compas.json_dump(
    model, Path(__file__).parent.parent / "data" / "grid_model.json", pretty=True
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

viewer.scene.add(
    [e.modelgeometry for e in columns],
    show_faces=True,
    opacity=0.7,
    name="Columns",
    hide_coplanaredges=True,
)
viewer.scene.add(
    [e.modelgeometry for e in beams],
    show_faces=True,
    name="Beams",
    hide_coplanaredges=True,
)
viewer.scene.add(
    [e.modelgeometry for e in blocks],
    show_faces=True,
    name="Blocks",
    hide_coplanaredges=True,
)


viewer.show()
