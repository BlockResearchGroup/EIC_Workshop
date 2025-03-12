from pathlib import Path

import compas
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Vector
from compas.tolerance import TOL

from compas_grid.elements import BeamProfileElement
from compas_grid.elements import CableElement
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

# Add beams
beams = []
for i in range(4, len(lines) - 2):
    beam = BeamProfileElement.from_t_profile(
        width=300,
        height=700,
        step_width_left=75,
        step_height_left=120,
        length=lines[i].length,
    )
    point = lines[i].start
    xaxis = Vector.Zaxis().cross(lines[i].vector)
    yaxis = Vector.Zaxis()
    target_frame = Frame(point, xaxis, yaxis)
    X = Transformation.from_frame_to_frame(Frame.worldXY(), target_frame)
    T = Translation.from_vector([0, beam.height * 0.5, 0])
    beam.transformation = X * T
    beam.extend(150)
    model.add_element(beam)
    beams.append(beam)

# Add cables
cables = []
for i in range(6, len(lines)):
    cable = CableElement(length=lines[i].length, radius=20)
    point = lines[i].start
    xaxis = Vector.Zaxis().cross(lines[i].vector)
    yaxis = Vector.Zaxis()
    target_frame = Frame(point, xaxis, yaxis)
    X = Transformation.from_frame_to_frame(Frame.worldXY(), target_frame)
    T = Translation.from_vector([0, beam.height * 0.0, 0])
    cable.transformation = X * T
    cable.extend(200)
    model.add_element(cable)
    cables.append(cable)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(model, Path(__file__).parent.parent / "data" / "model.json")

# =============================================================================
# Preprocess
# =============================================================================

TOL.lineardeflection = 1
TOL.angulardeflection = 1

elements = list(model.elements())

columns = [element for element in elements if isinstance(element, ColumnElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
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

viewer.scene.add(lines, linewidth=3, name="lines")

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in columns],
    show_faces=True,
    opacity=0.7,
    name="Columns",
)

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in beams],
    show_faces=True,
    opacity=0.7,
    name="Beams",
)

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in cables],
    show_faces=True,
    name="Cables",
)

viewer.show()
