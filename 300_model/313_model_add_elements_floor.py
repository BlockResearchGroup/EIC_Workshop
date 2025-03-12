from pathlib import Path

import compas
from compas.geometry import Translation
from compas.geometry import Scale
from compas.tolerance import TOL
from compas_grid.elements import BeamProfileElement
from compas_grid.elements import BlockElement
from compas_grid.elements import ColumnElement
from compas_grid.elements import CableElement
from compas_model.models import Model
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# Load Model
# =============================================================================

model: Model = compas.json_load(Path(__file__).parent.parent / "data" / "model.json")

# =============================================================================
# Make vault
# =============================================================================

barrel_vault_meshes = compas.json_load(
    Path(__file__).parent.parent / "data" / "floor_vault.json"
)

# =============================================================================
# Add vault blocks
# =============================================================================
for idx, mesh in enumerate(barrel_vault_meshes):
    grid_block = BlockElement(shape=mesh)
    grid_block.is_support = mesh.aabb().frame.point[2] < 25
    S = Scale.from_factors([1, 1, 1])
    T = Translation.from_vector([-1500, -2500, 2700])
    grid_block.transformation = T * S
    model.add_element(grid_block)


# =============================================================================
# Preprocess
# =============================================================================

TOL.lineardeflection = 1
TOL.angulardeflection = 1


elements = list(model.elements())
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
columns = [element for element in elements if isinstance(element, ColumnElement)]
blocks = [element for element in elements if isinstance(element, BlockElement)]
cables = [element for element in elements if isinstance(element, CableElement)]

# =============================================================================
# Export
# =============================================================================

compas.json_dump(model, Path(__file__).parent.parent / "data" / "model_with_floor.json")

# =============================================================================
# Visualize
# =============================================================================

config = Config()
config.camera.target = [0, 1000, 500]
config.camera.position = [0, -7000, 4000]
config.camera.scale = 1000
config.renderer.gridsize = (20000, 20, 20000, 20)
config.renderer.show_grid = False
viewer = Viewer(config=config)

viewer.scene.add(
    [e.modelgeometry for e in columns],
    show_faces=True,
    opacity=0.7,
    name="Columns",
)

viewer.scene.add(
    [e.modelgeometry for e in beams],
    show_faces=True,
    opacity=0.7,
    name="Beams",
    hide_coplanaredges=True,
)

viewer.scene.add(
    [e.modelgeometry for e in blocks],
    show_faces=True,
    opacity=0.7,
    name="Blocks",
)

viewer.scene.add(
    [e.modelgeometry for e in cables],
    show_faces=True,
    opacity=0.7,
    name="Cables",
    hide_coplanaredges=True,
)

viewer.show()
