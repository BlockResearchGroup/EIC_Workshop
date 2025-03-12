import pathlib

import compas
from compas.datastructures import Mesh
from compas.geometry import NurbsCurve
from compas_viewer import Viewer
from compas_viewer.config import Config

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# =============================================================================
# Session Import
# =============================================================================

session = compas.json_load(SESSION)

mesh: Mesh = session["tubemesh"]
path: list[int] = session["path"]
curve: NurbsCurve = session["curve"]

# =============================================================================
# Do
# =============================================================================

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
viewer.scene.add(mesh)
viewer.scene.add(curve, linewidth=3)
viewer.show()
