from pathlib import Path

import compas
from compas_model.models import Model
from compas_viewer import Viewer
from compas.geometry import Brep
from compas_viewer.config import Config
from compas_grid.elements import BeamProfileElement
from compas_grid.elements import ColumnElement
from compas_grid.elements import BlockElement
from compas.tolerance import TOL

# =============================================================================
# Load Model
# =============================================================================

model: Model = compas.json_load(Path(__file__).parent.parent / "data" / "model_with_modifiers.json")
# meshes = compas.json_load(Path(__file__).parent.parent / "data" / "structural_analysis_results.json")


# =============================================================================
# Preprocess
# =============================================================================

TOL.lineardeflection = 1
TOL.angulardeflection = 1

elements = list(model.elements())

columns = [element for element in elements if isinstance(element, ColumnElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
blocks = [element for element in elements if isinstance(element, BlockElement)]


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
    [e.modelgeometry for e in blocks],
    show_faces=True,
    name="Blocks",
)

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in columns],
    show_faces=True,
    opacity=0.7,
    name="Columns",
)

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in beams],
    show_faces=True,
    name="Beams",
)

viewer.show()
