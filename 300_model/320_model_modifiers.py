from pathlib import Path

import compas
from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.geometry import Polygon
from compas.geometry import distance_point_point
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

model: Model = compas.json_load(
    Path(__file__).parent.parent / "data" / "model_with_floor.json"
)

# =============================================================================
# Add Interactions
# =============================================================================

elements = list(model.elements())
blocks = [element for element in elements if isinstance(element, BlockElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
for beam in beams:
    for block in blocks:
        model.add_interaction(beam, block)
        model.add_modifier(beam, block)  # beam -> cuts -> block

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

compas.json_dump(
    model, Path(__file__).parent.parent / "data" / "model_with_modifiers.json"
)

# =============================================================================
# Visualize
# =============================================================================
config = Config()
config.camera.target = [0, 1000, 500]
config.camera.position = [0, -7000, 4000]
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
