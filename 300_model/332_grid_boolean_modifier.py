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
# Load Model
# =============================================================================

model: GridModel = compas.json_load(
    Path(__file__).parent.parent / "data" / "grid_model.json"
)

# =============================================================================
# Process elements
# =============================================================================
elements = list(model.elements())
columns = [element for element in elements if isinstance(element, ColumnElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
blocks = [element for element in elements if isinstance(element, BlockElement)]


# =============================================================================
# Add Interactions
# =============================================================================

elements = list(model.elements())
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
for beam in beams:
    for block in blocks:
        model.add_interaction(beam, block)
        model.add_modifier(beam, block)  # beam -> cuts -> block


# =============================================================================
# Export
# =============================================================================

compas.json_dump(
    model,
    Path(__file__).parent.parent / "data" / "grid_model_modifiers.json",
    pretty=True,
)

# =============================================================================
# Visualize
# =============================================================================

config = Config()
config.camera.target = [3000, 1000, 1250]
config.camera.position = [3000, -10000, 8125]
config.camera.scale = 1000
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
