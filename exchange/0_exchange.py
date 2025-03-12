import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas_viewer import Viewer
from compas_viewer.config import Config

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# =============================================================================
# Session Import
# =============================================================================

# =============================================================================
# Do
# =============================================================================

# construct a mesh from a sample OBJ file
mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

# assign a face attribute with name "is_selected" and value "False"
mesh.update_default_face_attributes(is_selected=False)

# select a random sample of faces
# and change the value of "is_selected" to "True"
faces = mesh.face_sample(size=17)
for face in faces:
    mesh.face_attribute(face, name="is_selected", value=True)

# =============================================================================
# Session Export
# =============================================================================

# store the mesh in a session dict
session = {"tubemesh": mesh}

compas.json_dump(session, SESSION)

# =============================================================================
# Visualisation
# =============================================================================

config = Config()
config.camera.position = [2, -5, 1]
config.camera.target = [2, 0, 1]

viewer = Viewer(config=config)
viewer.scene.add(mesh, facecolor={face: Color.pink() for face in faces})
viewer.show()
