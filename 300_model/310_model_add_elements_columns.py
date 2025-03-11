from pathlib import Path

import compas
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.tolerance import TOL

from compas_grid.elements import ColumnElement
from compas_model.models import Model
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# JSON file with the geometry of the model.
# =============================================================================
rhino_geometry = compas.json_load(
    Path(__file__).parent.parent / "data" / "model_input.json"
)
lines = rhino_geometry["lines"]

# =============================================================================
# Model
# =============================================================================

model = Model()

# =============================================================================
# Add Elements
# =============================================================================

# Add columns
for i in range(0, 4):
    column = ColumnElement(300, 300, lines[i].length)
    column.transformation = Transformation.from_frame_to_frame(
        Frame.worldXY(), Frame(lines[i].start)
    )
    model.add_element(column)

# =============================================================================
# Preprocess
# =============================================================================

TOL.lineardeflection = 1
TOL.angulardeflection = 1

elements = list(model.elements())

columns = [element for element in elements if isinstance(element, ColumnElement)]

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

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in columns],
    show_faces=True,
    opacity=0.7,
    name="Columns",
)

viewer.show()
