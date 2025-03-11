from pathlib import Path

import compas
from compas_grid.models import GridModel
from compas_grid.elements import BeamProfileElement
from compas_grid.elements import BlockElement
from compas_grid.elements import ColumnElement
from compas.geometry import Polygon
from compas_viewer import Viewer
from compas_viewer.config import Config
from compas.tolerance import TOL

# =============================================================================
# Load Model
# =============================================================================

model: GridModel = compas.json_load(
    Path(__file__).parent.parent / "data" / "grid_model_modifiers.json"
)

# =============================================================================
# Process elements
# =============================================================================
elements = list(model.elements())
columns = [element for element in elements if isinstance(element, ColumnElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
blocks = [element for element in elements if isinstance(element, BlockElement)]


# =============================================================================
# Compute Contacts
# =============================================================================

model.compute_contacts(tolerance=1, minimum_area=1, k=16)

contacts = []
for edge in model.graph.edges():
    if model.graph.edge_attribute(edge, "contacts"):
        for contact in model.graph.edge_attribute(edge, "contacts"):
            contacts.append(contact.mesh)


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
    show_faces=False,
    name="Beams",
    hide_coplanaredges=True,
)

viewer.scene.add(
    [e.modelgeometry for e in blocks],
    show_faces=False,
    name="Blocks",
    hide_coplanaredges=True,
)

viewer.scene.add(
    contacts,
    facecolor=(0, 255, 0),
    name="Contacts",
)


viewer.show()
