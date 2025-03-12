import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import NurbsCurve
from compas.geometry import Transformation
from compas.itertools import linspace
from compas_viewer import Viewer
from compas_viewer.config import Config

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"
MONKEY = HERE / "data" / "monkey.json"

# =============================================================================
# Session Import
# =============================================================================

session = compas.json_load(SESSION)

mesh: Mesh = session["tubemesh"]
path: list[int] = session["path"]
curve: NurbsCurve = session["curve"]

monkey: Mesh = compas.json_load(MONKEY)

# =============================================================================
# Do
# =============================================================================

monkey.scale(0.5)
monkey = monkey.subdivided(k=1)

frames: list[Frame] = []
for t in linspace(curve.domain[0], curve.domain[1], 100):
    frames.append(curve.frame_at(t))

transformations = []
for frame in frames:
    transformations.append(Transformation.from_frame_to_frame(frame.worldXY(), frame))

# =============================================================================
# Session Export
# =============================================================================

# compas.json_dump(session, SESSION)

# =============================================================================
# Visualisation
# =============================================================================

config = Config()
config.camera.position = [2, -5, 1]
config.camera.target = [2, 0, 1]

viewer = Viewer(config=config)
viewer.scene.add(mesh, opacity=0.5)
viewer.scene.add(curve, linewidth=3)

obj = viewer.scene.add(monkey, facecolor=Color.from_hex("#0092d2"))


@viewer.on(interval=100, frames=len(transformations))
def slide(f):
    obj.transformation = transformations[f]
    obj.update()


viewer.show()
