from pathlib import Path

import compas
from compas_model.models import Model
from compas_viewer import Viewer
from compas.geometry import Brep
from compas_viewer.config import Config
from compas_grid.elements import BeamProfileElement
from compas_grid.elements import ColumnElement
from compas_grid.elements import BlockElement
from compas_grid.elements import CableElement
from compas.tolerance import TOL

# =============================================================================
# Load Model
# =============================================================================

model: Model = compas.json_load(Path(__file__).parent.parent / "data" / "model_with_modifiers.json")
contact_forces = compas.json_load(Path(__file__).parent.parent / "data" / "Barrel_3dec.json")

for contact_force in contact_forces:
    contact_force.scale(1000)


# =============================================================================
# Preprocess
# =============================================================================

TOL.lineardeflection = 1
TOL.angulardeflection = 1

elements = list(model.elements())

columns = [element for element in elements if isinstance(element, ColumnElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
blocks = [element for element in elements if isinstance(element, BlockElement)]
cables = [element for element in elements if isinstance(element, CableElement)]


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
    show_faces=False,
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

viewer.scene.add(
    contact_forces,
    linewidth= 4,
    linecolor=(0,200,0),
    name="3DEC_contact_forces",
)

viewer.show()
